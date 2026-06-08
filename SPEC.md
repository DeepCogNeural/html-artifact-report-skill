# Artifact Report Contract

Version: `artifact-report.v1`

This contract defines how an agent produces a human-facing HTML report and a paired machine-readable JSON manifest.

## Outputs

Each completed artifact set contains:

- `artifact.html`
- `artifact.json`

The files must describe the same report. The HTML is optimized for a human reader. The JSON is optimized for agents and automation.

## HTML contract

`artifact.html` must:

- Be standalone HTML starting with `<!doctype html>`.
- Include `<meta name="artifact-contract" content="artifact-report.v1">`.
- Include `<meta name="artifact-id" content="...">` matching JSON `artifact_id`.
- Include readable report content, not a raw JSON dump.
- Use `data-section-id` for every major `<section>`.
- Use `data-component-id` for every meaningful visual, table, callout, evidence block, or command block.
- Register every HTML `data-section-id` and `data-component-id` in JSON exactly once.
- Include a reader-facing verification or limitations section.

## JSON contract

`artifact.json` is a manifest. It must not duplicate the full prose of the report.

Required fields:

```json
{
  "schema_version": "artifact-report.v1",
  "artifact_id": "stable-kebab-case-id",
  "title": "Report title",
  "template_version": "desktop-report-template.v1",
  "source_hashes": [
    {
      "path": "notes.md",
      "sha256": "64-character-lowercase-sha256"
    }
  ],
  "sections": [],
  "components": [],
  "claims": [],
  "evidence": [],
  "verification": {},
  "limitations": []
}
```

## ID alignment

Each `sections[].id` must appear in HTML as:

```html
<section data-section-id="same-id">
```

Each `components[].id` must appear in HTML as:

```html
<div data-component-id="same-id">
```

Other element types are allowed, but the `data-component-id` must be present.

The alignment is bidirectional:

- JSON IDs missing from HTML fail validation.
- HTML IDs missing from JSON fail validation.
- Duplicate IDs fail validation on either side.

## Claims and evidence

Use `claims[]` for statements that matter to the report decision.

Each claim should include:

- `id`
- `text`
- `status`: `supported`, `partial`, or `unsupported`
- `evidence_ids`

Use `evidence[]` for sources, commands, files, datasets, or observations.

Each evidence item should include:

- `id`
- `kind`
- `summary`
- `source`

If `source` points to a local file, that file must also appear in `source_hashes`.

## Verification

`verification` records what was checked.

Minimum fields:

- `status`: `passed`, `failed`, or `partial`
- `checks`: list of commands or checks
- `checked_at`: ISO-like timestamp or date

The HTML must include a corresponding verification section for the reader.

## Limitations

Use `limitations[]` for missing data, unverified assumptions, stale inputs, partial checks, or risks that remain after verification.

Do not hide uncertainty in the JSON.

## Generated artifact license note

Generated HTML may contain template HTML/CSS from this repository. Users may distribute generated reports under their own content license as long as they comply with this repository's MIT license for included template code.
