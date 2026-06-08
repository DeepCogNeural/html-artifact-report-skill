---
name: html-artifact-report
description: Create HTML report artifacts from notes or Markdown with paired JSON manifests for AI-agent audit and reuse.
category: reporting
tags: ["html", "report", "artifact", "json", "manifest", "markdown", "ai-agent", "evidence"]
---

# HTML Report Artifact

Use this skill when a substantial answer, review, analysis, decision memo, or research summary should become a durable artifact instead of a long chat response.

Produce exactly two primary outputs:

- `artifact.html` — the human-facing report.
- `artifact.json` — the agent-facing manifest.

The JSON manifest is not a prose duplicate. It is a structured record of sections, components, claims, evidence, limitations, source hashes, and verification.

## Files to read first

Resolve paths relative to this `SKILL.md`.

1. `SPEC.md` — the public contract.
2. `templates/desktop-report-template.html` — the canonical HTML baseline.
3. `components/report-components.md` — allowed report components.
4. `references/anti-slop.md` — visual anti-patterns to avoid.
5. One complete example under `examples/`.

## Workflow

1. Identify the reader, decision, evidence, and source material.
2. Draft the semantic outline before writing HTML:
   - summary
   - sections
   - components
   - claims
   - evidence
   - verification
   - limitations
3. Create `artifact.json` from the outline.
4. Create `artifact.html` from `templates/desktop-report-template.html`.
5. Ensure HTML and JSON section IDs match exactly, with no duplicates or unregistered extras.
6. Ensure HTML and JSON component IDs match exactly, with no duplicates or unregistered extras.
7. Hash every local evidence file listed in `artifact.json`.
8. Run:

```bash
python3 scripts/check_html_artifact.py artifact.html
python3 scripts/check_artifact_json.py artifact.json --html artifact.html
```

For repository examples, run:

```bash
python3 scripts/check_examples.py
python3 -m unittest discover -s tests
```

## HTML requirements

- Start with `<!doctype html>`.
- Include `<meta name="artifact-contract" content="artifact-report.v1">`.
- Use a single `.page` main column at `max-width:1180px`.
- Use the canonical font tokens:
  - `--serif: ui-serif, Georgia, "Times New Roman", serif`
  - `--sans: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`
  - `--mono: ui-monospace, "SF Mono", Menlo, Monaco, monospace`
- Use the canonical warm palette tokens:
  - `#FAF9F5`
  - `#141413`
  - `#D97757`
- Include:
  - answer-first TL;DR
  - summary cards
  - real sections
  - at least one visual or table
  - folded evidence
  - verification and limitations

## JSON requirements

The manifest must validate against `contract/artifact-report.schema.json`.

Required top-level fields:

- `schema_version`
- `artifact_id`
- `title`
- `template_version`
- `source_hashes`
- `sections`
- `components`
- `claims`
- `evidence`
- `verification`
- `limitations`

## Style rules

- Be answer-first.
- Keep dense raw evidence folded behind `<details>`.
- Do not invent data.
- Label missing evidence clearly.
- Do not show format-compliance notes to the reader.
- Do not add a sticky sidebar, a default table of contents, or tab-hidden main content.
- Do not use decorative emoji as structural icons.
- Do not use purple gradients, neon colors, GitHub-dark `#0D1117`, or generic SaaS dashboard shells.
