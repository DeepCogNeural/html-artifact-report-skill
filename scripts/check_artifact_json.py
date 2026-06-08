#!/usr/bin/env python3
"""Validate artifact-report JSON and optionally cross-check it against HTML."""

from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = REPO_ROOT / "contract" / "artifact-report.schema.json"


class HTMLIdParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.section_id_list: list[str] = []
        self.component_id_list: list[str] = []
        self.section_ids: set[str] = set()
        self.component_ids: set[str] = set()
        self.meta: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        if tag == "meta" and "name" in attr:
            self.meta[attr["name"]] = attr.get("content", "")
        if "data-section-id" in attr:
            self.section_id_list.append(attr["data-section-id"])
            self.section_ids.add(attr["data-section-id"])
        if "data-component-id" in attr:
            self.component_id_list.append(attr["data-component-id"])
            self.component_ids.add(attr["data-component-id"])


def _type_ok(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    return True


def _validate_schema(value: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    failures: list[str] = []

    expected_type = schema.get("type")
    if isinstance(expected_type, str) and not _type_ok(value, expected_type):
        return [f"{path}: expected {expected_type}, got {type(value).__name__}"]

    if "const" in schema and value != schema["const"]:
        failures.append(f"{path}: expected const {schema['const']!r}")

    if "enum" in schema and value not in schema["enum"]:
        failures.append(f"{path}: expected one of {schema['enum']!r}")

    if isinstance(value, str):
        if "minLength" in schema and len(value) < int(schema["minLength"]):
            failures.append(f"{path}: string shorter than minLength")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            failures.append(f"{path}: does not match pattern {schema['pattern']!r}")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < int(schema["minItems"]):
            failures.append(f"{path}: array shorter than minItems")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(value):
                failures.extend(_validate_schema(item, item_schema, f"{path}[{index}]"))

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                failures.append(f"{path}: missing required key {key!r}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    failures.append(f"{path}: unexpected key {key!r}")
        for key, child_schema in properties.items():
            if key in value and isinstance(child_schema, dict):
                failures.extend(_validate_schema(value[key], child_schema, f"{path}.{key}"))

    return failures


def _load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _resolve_source_path(source_path: str, manifest_path: Path) -> Path | None:
    path = Path(source_path)
    candidates = [path] if path.is_absolute() else [REPO_ROOT / path, manifest_path.parent / path]
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def validate_manifest(manifest_path: Path, *, schema_path: Path = DEFAULT_SCHEMA, html_path: Path | None = None) -> list[str]:
    manifest = _load_json(manifest_path)
    schema = _load_json(schema_path)
    failures = _validate_schema(manifest, schema)
    if failures:
        return failures

    section_id_list = [section["id"] for section in manifest["sections"]]
    component_id_list = [component["id"] for component in manifest["components"]]
    evidence_id_list = [evidence["id"] for evidence in manifest["evidence"]]
    claim_id_list = [claim["id"] for claim in manifest["claims"]]
    section_ids = set(section_id_list)
    component_ids = set(component_id_list)
    evidence_ids = set(evidence_id_list)

    for name, values in [
        ("sections", section_id_list),
        ("components", component_id_list),
        ("evidence", evidence_id_list),
        ("claims", claim_id_list),
    ]:
        duplicate_ids = _duplicates(values)
        if duplicate_ids:
            failures.append(f"$.{name}: duplicate ids {duplicate_ids}")

    for source in manifest["source_hashes"]:
        resolved = _resolve_source_path(source["path"], manifest_path)
        if resolved is None:
            failures.append(f"$.source_hashes[{source['path']}]: source file not found")
            continue
        actual = _sha256(resolved)
        if actual != source["sha256"]:
            failures.append(f"$.source_hashes[{source['path']}]: sha256 mismatch, got {actual}")

    hashed_paths = {source["path"] for source in manifest["source_hashes"]}
    for evidence in manifest["evidence"]:
        resolved = _resolve_source_path(evidence["source"], manifest_path)
        if resolved is not None and evidence["source"] not in hashed_paths:
            failures.append(f"$.evidence[{evidence['id']}]: local source {evidence['source']!r} is not listed in source_hashes")

    for component in manifest["components"]:
        if component["section_id"] not in section_ids:
            failures.append(f"$.components[{component['id']}]: unknown section_id {component['section_id']!r}")

    for claim in manifest["claims"]:
        for evidence_id in claim["evidence_ids"]:
            if evidence_id not in evidence_ids:
                failures.append(f"$.claims[{claim['id']}]: unknown evidence_id {evidence_id!r}")

    if html_path is not None:
        parser = HTMLIdParser()
        parser.feed(html_path.read_text(encoding="utf-8"))
        if parser.meta.get("artifact-contract") != manifest["schema_version"]:
            failures.append("html: artifact-contract meta does not match schema_version")
        if parser.meta.get("artifact-id") != manifest["artifact_id"]:
            failures.append("html: artifact-id meta does not match artifact_id")
        duplicate_html_sections = _duplicates(parser.section_id_list)
        duplicate_html_components = _duplicates(parser.component_id_list)
        if duplicate_html_sections:
            failures.append(f"html: duplicate data-section-id values {duplicate_html_sections}")
        if duplicate_html_components:
            failures.append(f"html: duplicate data-component-id values {duplicate_html_components}")
        missing_sections = sorted(section_ids - parser.section_ids)
        extra_sections = sorted(parser.section_ids - section_ids)
        missing_components = sorted(component_ids - parser.component_ids)
        extra_components = sorted(parser.component_ids - component_ids)
        if missing_sections:
            failures.append(f"html: missing data-section-id values {missing_sections}")
        if extra_sections:
            failures.append(f"html: unregistered data-section-id values {extra_sections}")
        if missing_components:
            failures.append(f"html: missing data-component-id values {missing_components}")
        if extra_components:
            failures.append(f"html: unregistered data-component-id values {extra_components}")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json", type=Path)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--html", type=Path)
    args = parser.parse_args()

    failures = validate_manifest(args.json, schema_path=args.schema, html_path=args.html)
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print(f"ok {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
