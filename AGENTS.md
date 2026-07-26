# Agent Guide

This repository contains one agent skill: `html-artifact-report`.

## What to read first

Contract: `SPEC.md`. Runtime: `SKILL.md`. Allowed components: `components/report-components.md`. Examples show the shape.

## Core rule

The output is always two aligned files:

- `artifact.html` for humans.
- `artifact.json` for agents and automation.

Do not create a pretty HTML report without a manifest. Do not create a manifest that cannot be cross-checked against the HTML.

## Verification

Run the verification commands listed in `SKILL.md` before saying done.

## Editing rules

- Keep v1 focused on one canonical report profile.
- Do not add a GUI app, live preview server, social-card templates, or document conversion pipeline.
- Keep examples real enough to validate the contract.
- Add negative fixtures when tightening a checker.
- If a local evidence file is cited in `artifact.json`, include it in `source_hashes`.
