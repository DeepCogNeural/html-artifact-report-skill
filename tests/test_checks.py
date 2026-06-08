import json
from pathlib import Path
import tempfile
import unittest

from scripts.check_artifact_json import validate_manifest
from scripts.check_html_artifact import check_html


ROOT = Path(__file__).resolve().parents[1]


class ArtifactChecksTest(unittest.TestCase):
    def test_examples_pass(self) -> None:
        for example_dir in sorted((ROOT / "examples").iterdir()):
            if not example_dir.is_dir():
                continue
            with self.subTest(example=example_dir.name):
                html = example_dir / "artifact.html"
                manifest = example_dir / "artifact.json"
                self.assertEqual(check_html(html), [])
                self.assertEqual(validate_manifest(manifest, html_path=html), [])

    def test_bad_slop_fails_html_check(self) -> None:
        failures = check_html(ROOT / "tests" / "fixtures" / "bad-slop" / "artifact.html")
        self.assertTrue(any("no_purple_gradient" in failure for failure in failures))
        self.assertTrue(any("no_required_tabs" in failure for failure in failures))

    def test_drift_fails_cross_check(self) -> None:
        failures = validate_manifest(
            ROOT / "tests" / "fixtures" / "drift" / "artifact.json",
            html_path=ROOT / "tests" / "fixtures" / "drift" / "artifact.html",
        )
        self.assertTrue(any("missing data-section-id" in failure for failure in failures))
        self.assertTrue(any("missing data-component-id" in failure for failure in failures))

    def test_duplicate_manifest_ids_fail(self) -> None:
        source = ROOT / "examples" / "executive-decision-brief" / "artifact.json"
        data = json.loads(source.read_text(encoding="utf-8"))
        data["sections"].append(dict(data["sections"][0]))
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "artifact.json"
            manifest.write_text(json.dumps(data), encoding="utf-8")
            failures = validate_manifest(
                manifest,
                html_path=ROOT / "examples" / "executive-decision-brief" / "artifact.html",
            )
        self.assertTrue(any("duplicate ids" in failure for failure in failures))

    def test_unregistered_html_component_fails(self) -> None:
        html_source = ROOT / "examples" / "executive-decision-brief" / "artifact.html"
        html_text = html_source.read_text(encoding="utf-8").replace(
            "</main>",
            '<div data-component-id="cmp-unregistered">extra</div></main>',
        )
        with tempfile.TemporaryDirectory() as tmp:
            html = Path(tmp) / "artifact.html"
            html.write_text(html_text, encoding="utf-8")
            failures = validate_manifest(
                ROOT / "examples" / "executive-decision-brief" / "artifact.json",
                html_path=html,
            )
        self.assertTrue(any("unregistered data-component-id" in failure for failure in failures))

    def test_duplicate_html_component_fails(self) -> None:
        html_source = ROOT / "examples" / "executive-decision-brief" / "artifact.html"
        html_text = html_source.read_text(encoding="utf-8").replace(
            "</main>",
            '<div data-component-id="cmp-tldr">duplicate</div></main>',
        )
        with tempfile.TemporaryDirectory() as tmp:
            html = Path(tmp) / "artifact.html"
            html.write_text(html_text, encoding="utf-8")
            failures = validate_manifest(
                ROOT / "examples" / "executive-decision-brief" / "artifact.json",
                html_path=html,
            )
        self.assertTrue(any("duplicate data-component-id" in failure for failure in failures))

    def test_missing_source_hash_path_fails(self) -> None:
        source = ROOT / "examples" / "executive-decision-brief" / "artifact.json"
        data = json.loads(source.read_text(encoding="utf-8"))
        data["source_hashes"][0]["path"] = "missing/input.md"
        data["evidence"][0]["source"] = "missing/input.md"
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "artifact.json"
            manifest.write_text(json.dumps(data), encoding="utf-8")
            failures = validate_manifest(manifest)
        self.assertTrue(any("source file not found" in failure for failure in failures))

    def test_unhashed_local_evidence_source_fails(self) -> None:
        source = ROOT / "examples" / "executive-decision-brief" / "artifact.json"
        data = json.loads(source.read_text(encoding="utf-8"))
        data["source_hashes"] = data["source_hashes"][:1]
        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / "artifact.json"
            manifest.write_text(json.dumps(data), encoding="utf-8")
            failures = validate_manifest(manifest)
        self.assertTrue(any("is not listed in source_hashes" in failure for failure in failures))

    def test_missing_type_scale_fails(self) -> None:
        html = (ROOT / "examples" / "executive-decision-brief" / "artifact.html").read_text(encoding="utf-8")
        html = html.replace("h1 { margin:0 0 18px; font-size:38px; }", "h1 { margin:0 0 18px; }")
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "artifact.html"
            path.write_text(html, encoding="utf-8")
            failures = check_html(path)
        self.assertTrue(any("canonical_type_scale" in failure for failure in failures))

    def test_open_details_fail(self) -> None:
        html = (ROOT / "examples" / "executive-decision-brief" / "artifact.html").read_text(encoding="utf-8")
        html = html.replace('<details data-component-id="cmp-raw-evidence">', '<details open data-component-id="cmp-raw-evidence">')
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "artifact.html"
            path.write_text(html, encoding="utf-8")
            failures = check_html(path)
        self.assertTrue(any("no_open_details" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
