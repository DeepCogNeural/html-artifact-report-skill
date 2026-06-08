#!/usr/bin/env python3
"""Static checks for warm editorial artifact-report HTML files."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import sys


class ArtifactHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.detail_depth = 0
        self.current_table: dict[str, int | bool] | None = None
        self.tables: list[dict[str, int | bool]] = []
        self._current_cols = 0
        self.section_ids: set[str] = set()
        self.component_ids: set[str] = set()
        self.meta: dict[str, str] = {}
        self.has_open_details = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        if tag == "meta" and "name" in attr:
            self.meta[attr["name"]] = attr.get("content", "")
        if "data-section-id" in attr:
            self.section_ids.add(attr["data-section-id"])
        if "data-component-id" in attr:
            self.component_ids.add(attr["data-component-id"])
        if tag == "details":
            if "open" in attr:
                self.has_open_details = True
            self.detail_depth += 1
        elif tag == "table":
            self.current_table = {
                "rows": 0,
                "max_cols": 0,
                "in_details": self.detail_depth > 0,
            }
            self.tables.append(self.current_table)
        elif tag == "tr" and self.current_table is not None:
            self.current_table["rows"] = int(self.current_table["rows"]) + 1
            self._current_cols = 0
        elif tag in {"td", "th"} and self.current_table is not None:
            self._current_cols += 1
            self.current_table["max_cols"] = max(int(self.current_table["max_cols"]), self._current_cols)

    def handle_endtag(self, tag: str) -> None:
        if tag == "table":
            self.current_table = None
        elif tag == "details" and self.detail_depth:
            self.detail_depth -= 1


def _css_rule_body(text: str, selector: str) -> str:
    match = re.search(rf"{re.escape(selector)}\s*\{{(?P<body>[^}}]*)\}}", text, re.S)
    return match.group("body") if match else ""


def _css_value(rule_body: str, prop: str) -> str:
    match = re.search(rf"{re.escape(prop)}\s*:\s*([^;]+)", rule_body)
    return re.sub(r"\s+", " ", match.group(1)).strip() if match else ""


def _font_size_px(rule_body: str) -> float | None:
    match = re.search(r"font-size\s*:\s*(?P<size>\d+(?:\.\d+)?)px", rule_body)
    return float(match.group("size")) if match else None


def _max_width_px(rule_body: str) -> float | None:
    match = re.search(r"max-width\s*:\s*(?P<size>\d+(?:\.\d+)?)px", rule_body)
    return float(match.group("size")) if match else None


def _has_var(text: str, name: str, expected: str) -> bool:
    match = re.search(rf"{re.escape(name)}\s*:\s*([^;]+);", text)
    if not match:
        return False
    return re.sub(r"\s+", " ", match.group(1)).strip() == expected


def check_html(path: Path, *, min_sections: int = 4) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lower = text.lower()
    parsed = ArtifactHTMLParser()
    parsed.feed(text)

    failures: list[str] = []

    def require(name: str, ok: bool, message: str) -> None:
        if not ok:
            failures.append(f"{name}: {message}")

    body_rule = _css_rule_body(text, "body")
    header_rule = _css_rule_body(text, "header")
    tldr_rule = _css_rule_body(text, ".tldr")
    summary_rule = _css_rule_body(text, ".summary")
    h1_size = _font_size_px(_css_rule_body(text, "h1"))
    h2_size = _font_size_px(_css_rule_body(text, "h2"))
    body_size = _font_size_px(body_rule)
    page_width = _max_width_px(_css_rule_body(text, ".page"))
    section_count = len(re.findall(r"<section\b", lower))
    long_visible_tables = [
        table
        for table in parsed.tables
        if not table["in_details"] and (int(table["rows"]) > 6 or int(table["max_cols"]) > 4)
    ]
    has_side_toc = bool(
        re.search(r"<aside\b", lower)
        or re.search(r"position\s*:\s*sticky", lower)
        or re.search(r"grid-template-columns\s*:[^;]*(?:\b2[0-9]{2}px|\b3[0-9]{2}px)", lower)
    )
    narrow_top_blocks: list[tuple[str, float]] = []
    if page_width is not None:
        for selector in ["header", "main", "h1", ".prompt-box", ".tldr", ".summary"]:
            max_width = _max_width_px(_css_rule_body(text, selector))
            if max_width is not None and max_width < page_width - 1:
                narrow_top_blocks.append((selector, max_width))

    require("doctype", lower.lstrip().startswith("<!doctype html>"), "file must start with <!doctype html>")
    require("viewport", 'name="viewport"' in lower or "name='viewport'" in lower, "missing viewport meta")
    require(
        "contract_meta",
        parsed.meta.get("artifact-contract") == "artifact-report.v1",
        "missing artifact contract meta",
    )
    require("artifact_id_meta", bool(parsed.meta.get("artifact-id")), "missing artifact-id meta")
    require("warm_palette", all(color in text for color in ["#FAF9F5", "#141413", "#D97757"]), "missing canonical palette")
    require("font_tokens", all(token in text for token in ["--serif", "--sans", "--mono"]), "missing font tokens")
    require(
        "canonical_font_stacks",
        _has_var(text, "--serif", 'ui-serif, Georgia, "Times New Roman", serif')
        and _has_var(text, "--sans", 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif')
        and _has_var(text, "--mono", 'ui-monospace, "SF Mono", Menlo, Monaco, monospace'),
        "font stacks must match the canonical profile",
    )
    require(
        "canonical_type_scale",
        h1_size == 38 and h2_size == 26 and body_size == 15,
        f"expected body=15px h1=38px h2=26px, got body={body_size} h1={h1_size} h2={h2_size}",
    )
    require(
        "canonical_spacing",
        _css_value(body_rule, "padding") == "56px 32px 120px"
        and _css_value(header_rule, "margin-bottom") == "10px"
        and _css_value(tldr_rule, "margin") == "10px 0 34px"
        and _css_value(tldr_rule, "padding") == "22px 26px"
        and (_css_value(summary_rule, "margin-bottom") == "60px" or _css_value(summary_rule, "margin") == "0 0 60px"),
        "spacing must match canonical profile",
    )
    require("tldr", 'class="tldr"' in text or "TL;DR" in text, "missing answer-first TL;DR")
    require("summary", 'class="summary"' in text, "missing summary cards")
    require("real_sections", section_count >= min_sections, f"expected at least {min_sections} sections")
    require("section_ids", len(parsed.section_ids) >= min_sections, "sections need data-section-id")
    require("component_ids", bool(parsed.component_ids), "components need data-component-id")
    require("visual_or_table", "<svg" in lower or "<canvas" in lower or "<table" in lower, "expected visual or table")
    require("folded_evidence", "<details" in lower, "expected folded evidence")
    require("no_open_details", not parsed.has_open_details, "folded evidence must not be open by default")
    require("copy_affordance", "data-copy" in text or "clipboard.writeText" in text, "expected copy affordance")
    require("verification", "Verification" in text or "verification" in lower, "missing verification content")
    require("limitations", "Limitations" in text or "limitations" in lower, "missing limitations content")
    require("no_required_tabs", ".tabs" not in text and "tab-panel" not in text and 'role="tablist"' not in lower, "main content must not be hidden behind tabs")
    require("no_side_toc", not has_side_toc, "default report must not include sticky sidebars or side TOC")
    require("no_long_visible_tables", not long_visible_tables, f"long visible tables must be folded: {long_visible_tables}")
    require("aligned_top_blocks", not narrow_top_blocks, f"top blocks should share page width: {narrow_top_blocks}")
    require("no_placeholders", not re.search(r"\{\{[^}]+\}\}|lorem ipsum|your text here", lower), "leftover placeholder text")
    require("no_purple_gradient", "linear-gradient(135deg, #667eea, #764ba2)" not in lower, "purple gradient is forbidden")
    require("no_github_dark_shell", "#0d1117" not in lower, "GitHub-dark shell is forbidden")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path)
    parser.add_argument("--min-sections", type=int, default=4)
    args = parser.parse_args()

    failures = check_html(args.html, min_sections=args.min_sections)
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        return 1
    print(f"ok {args.html}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
