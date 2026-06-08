# Agent Guide

This repository contains one agent skill: `html-artifact-report`.

## What to read first

1. `README.md` for positioning and quickstart.
2. `SPEC.md` for the artifact contract.
3. `SKILL.md` for runtime instructions.
4. `components/report-components.md` for allowed components.
5. One complete example under `examples/`.

## Core rule

The output is always two aligned files:

- `artifact.html` for humans.
- `artifact.json` for agents and automation.

Do not create a pretty HTML report without a manifest. Do not create a manifest that cannot be cross-checked against the HTML.

## Verification

Run these before saying done:

```bash
python3 scripts/check_examples.py
python3 -m unittest discover -s tests
```

For a single artifact:

```bash
python3 scripts/check_html_artifact.py artifact.html
python3 scripts/check_artifact_json.py artifact.json --html artifact.html
```

## Editing rules

- Keep v1 focused on one canonical report profile.
- Do not add a GUI app, live preview server, social-card templates, or document conversion pipeline.
- Keep examples real enough to validate the contract.
- Add negative fixtures when tightening a checker.
- If a local evidence file is cited in `artifact.json`, include it in `source_hashes`.

