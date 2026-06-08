# HTML Artifact Report Skill

An agent skill for producing warm editorial single-file HTML reports with a paired machine-readable JSON manifest.

The skill has one job: turn substantial analysis into two aligned artifacts:

- `artifact.html` for humans.
- `artifact.json` for agents, automation, review, and regression checks.

It is not a web app, a template marketplace, a Markdown converter, or a document pipeline.

## Contract in 60 seconds

Every completed report must include:

1. A standalone `artifact.html` file.
2. A paired `artifact.json` file that validates against `contract/artifact-report.schema.json`.
3. Matching IDs between both files:
   - HTML sections use `data-section-id`.
   - HTML components use `data-component-id`.
   - JSON `sections[].id` and `components[].id` must exist in the HTML.
4. A verification record in JSON and a reader-facing verification section in HTML.

The JSON file is a manifest, not a second prose report. It records the report outline, evidence, claims, limitations, source hashes, and verification status so another agent can audit or reuse the artifact without scraping the page.

## Install

Copy or symlink this repository into your agent skill directory, or reference `SKILL.md` from your agent workflow.

For Codex-style local skills:

```bash
ln -s /path/to/html-artifact-report-skill ~/.codex/skills/html-artifact-report
```

## Use

Ask your agent to use the skill when a response would be better as a durable report:

```text
Use html-artifact-report to create a decision report from notes.md.
Write both artifact.html and artifact.json, then run scripts/check_examples.py.
```

For one artifact:

```bash
python3 scripts/check_html_artifact.py examples/executive-decision-brief/artifact.html
python3 scripts/check_artifact_json.py examples/executive-decision-brief/artifact.json --html examples/executive-decision-brief/artifact.html
```

For all examples:

```bash
python3 scripts/check_examples.py
python3 -m unittest discover -s tests
```

## Design position

This skill defaults to one canonical profile: warm editorial single-file HTML reports.

The report should be answer-first, readable, and evidence-aware:

- One wide main column.
- Warm low-saturation palette.
- Serif editorial headings.
- Structured summary cards.
- Real visuals or tables when they help.
- Folded raw evidence for long details.
- A clear verification and limitations section.

Avoid generic AI-looking output: purple gradients, decorative emoji as structure, dark blue SaaS shells, sticky sidebars, hidden tab content, and large raw tables dumped into the main flow.

## Repository layout

```text
.
├── SKILL.md
├── SPEC.md
├── contract/
│   ├── artifact-report.schema.json
│   └── artifact-report.example.json
├── templates/
│   └── desktop-report-template.html
├── components/
│   └── report-components.md
├── references/
│   ├── anti-slop.md
│   └── style-principles.md
├── examples/
│   └── */{input.md,artifact.html,artifact.json}
├── scripts/
│   ├── check_html_artifact.py
│   ├── check_artifact_json.py
│   └── check_examples.py
└── tests/
```

## License

MIT. Generated artifacts may include template HTML/CSS from this repository; see `LICENSE` and `ATTRIBUTIONS.md`.

