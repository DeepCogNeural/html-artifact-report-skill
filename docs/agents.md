# Install HTML Report Skill for AI Agents

This guide shows how to install or use `html-artifact-report` across common coding-agent setups.

The skill always produces two aligned files:

- `artifact.html`: the standalone report for human readers.
- `artifact.json`: the manifest for agents, automation, and verification.

## Recommended: npx skills

List skills in this repository:

```bash
npx skills add DeepCogNeural/html-artifact-report-skill --list
```

Install for the agent you actually use. Do not start with `--agent '*'`; some clients do not support global skill installation.

Claude Code:

```bash
npx skills add DeepCogNeural/html-artifact-report-skill \
  --agent claude-code \
  --skill html-artifact-report \
  -g -y
```

Codex:

```bash
npx skills add DeepCogNeural/html-artifact-report-skill \
  --agent codex \
  --skill html-artifact-report \
  -g -y
```

Generate a one-off prompt without installing:

```bash
npx skills use DeepCogNeural/html-artifact-report-skill@html-artifact-report
```

## Claude Code

Install:

```bash
npx skills add DeepCogNeural/html-artifact-report-skill \
  --agent claude-code \
  --skill html-artifact-report \
  -g -y
```

Manual fallback:

```bash
git clone https://github.com/DeepCogNeural/html-artifact-report-skill.git
mkdir -p ~/.claude/skills
ln -s "$PWD/html-artifact-report-skill" ~/.claude/skills/html-artifact-report
```

First prompt:

```text
Use the html-artifact-report skill.
Turn notes.md into artifact.html and artifact.json.
Read SPEC.md and one complete example first.
Run both checkers before reporting done.
```

## Codex

Install:

```bash
npx skills add DeepCogNeural/html-artifact-report-skill \
  --agent codex \
  --skill html-artifact-report \
  -g -y
```

Manual fallback:

```bash
git clone https://github.com/DeepCogNeural/html-artifact-report-skill.git
mkdir -p ~/.codex/skills
ln -s "$PWD/html-artifact-report-skill" ~/.codex/skills/html-artifact-report
```

First prompt:

```text
Use html-artifact-report.
Read SKILL.md, SPEC.md, templates/desktop-report-template.html,
components/report-components.md, and one complete example.
Create artifact.html and artifact.json.
Run:
python3 scripts/check_html_artifact.py artifact.html
python3 scripts/check_artifact_json.py artifact.json --html artifact.html
```

## Cursor

Install:

```bash
npx skills add DeepCogNeural/html-artifact-report-skill \
  --agent cursor \
  --skill html-artifact-report \
  -g -y
```

Fallback: keep this repository in the project and reference `SKILL.md` from Cursor's agent instructions.

First prompt:

```text
Use the html-artifact-report repository instructions.
Do not write a Markdown-only report.
Produce artifact.html and artifact.json.
The JSON is a manifest, not another prose report.
```

## Gemini CLI

If your Gemini CLI setup supports skills through `npx skills`, use:

```bash
npx skills add DeepCogNeural/html-artifact-report-skill \
  --agent gemini-cli \
  --skill html-artifact-report \
  -g -y
```

If not, use the one-off prompt route:

```bash
npx skills use DeepCogNeural/html-artifact-report-skill@html-artifact-report
```

Paste the generated instruction into Gemini CLI and point it at this repository.

First prompt:

```text
Use this repo as a file-based agent skill.
Follow SKILL.md exactly.
Output artifact.html and artifact.json.
Validate the pair with the Python checkers.
```

## DeepSeek-backed agents

DeepSeek is a model/API provider, not a single skill installation location. Use the installation path for the client that is running DeepSeek:

- Cursor with a DeepSeek model: use the Cursor section.
- Cline, Continue, OpenCode, or similar clients: keep this repo in the workspace and paste the one-off prompt from `npx skills use`.
- Any terminal agent: point it at `SKILL.md`, `SPEC.md`, `templates/desktop-report-template.html`, `components/report-components.md`, and one example.

Minimal prompt:

```text
You are using a DeepSeek model inside my coding agent.
Use the html-artifact-report skill from this repository.
Read SKILL.md, SPEC.md, templates/desktop-report-template.html,
components/report-components.md, and one example.
Produce artifact.html and artifact.json.
Validate with scripts/check_html_artifact.py and scripts/check_artifact_json.py.
```

## Generic agent fallback

Any agent that can read files and run Python can use the skill:

```bash
git clone https://github.com/DeepCogNeural/html-artifact-report-skill.git
cd html-artifact-report-skill
```

Then prompt:

```text
Use this repository as an agent skill.
Follow SKILL.md exactly.
The final report must include artifact.html and artifact.json.
The JSON is a manifest, not a prose duplicate.
Run python3 scripts/check_examples.py after any repository changes.
```

## Verification

For one artifact pair:

```bash
python3 scripts/check_html_artifact.py artifact.html
python3 scripts/check_artifact_json.py artifact.json --html artifact.html
```

For this repository:

```bash
python3 scripts/check_examples.py
python3 -m unittest discover -s tests
```

## Common mistakes

- Creating only `artifact.html`.
- Writing `artifact.json` as another essay instead of a manifest.
- Letting JSON section/component IDs drift from HTML `data-*` IDs.
- Showing raw long tables on the first screen instead of folding evidence.
- Adding a sidebar, purple gradient, tab-hidden report body, or generic SaaS dashboard shell.
