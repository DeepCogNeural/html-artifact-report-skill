#!/usr/bin/env python3
"""Run repository example and negative-fixture checks."""

from __future__ import annotations

from pathlib import Path
import sys

from check_artifact_json import validate_manifest
from check_html_artifact import check_html


ROOT = Path(__file__).resolve().parents[1]


def _expect_pass(name: str, failures: list[str]) -> int:
    if failures:
        print(f"FAIL {name}")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"ok {name}")
    return 0


def _expect_fail(name: str, failures: list[str], expected: list[str] | None = None) -> int:
    if failures:
        if expected:
            missing = [needle for needle in expected if not any(needle in failure for failure in failures)]
            if missing:
                print(f"FAIL negative {name}: missing expected failures {missing}")
                for failure in failures:
                    print(f"  - {failure}")
                return 1
        print(f"ok negative {name}")
        return 0
    print(f"FAIL negative {name}: checker unexpectedly passed")
    return 1


def main() -> int:
    status = 0
    for example_dir in sorted((ROOT / "examples").iterdir()):
        if not example_dir.is_dir():
            continue
        html = example_dir / "artifact.html"
        manifest = example_dir / "artifact.json"
        if not html.exists() or not manifest.exists():
            print(f"FAIL {example_dir.name}: missing artifact.html or artifact.json")
            status = 1
            continue
        status |= _expect_pass(f"{example_dir.name} html", check_html(html))
        status |= _expect_pass(
            f"{example_dir.name} json",
            validate_manifest(manifest, html_path=html),
        )

    bad_slop = ROOT / "tests" / "fixtures" / "bad-slop" / "artifact.html"
    bad_drift_json = ROOT / "tests" / "fixtures" / "drift" / "artifact.json"
    bad_drift_html = ROOT / "tests" / "fixtures" / "drift" / "artifact.html"
    status |= _expect_fail(
        "bad-slop html",
        check_html(bad_slop),
        ["no_purple_gradient", "no_required_tabs"],
    )
    status |= _expect_fail(
        "drift json/html",
        validate_manifest(bad_drift_json, html_path=bad_drift_html),
        ["missing data-section-id", "missing data-component-id"],
    )
    return status


if __name__ == "__main__":
    sys.exit(main())
