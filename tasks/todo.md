# Current Task

Goal: make the README first screen explain the product and language navigation immediately.

## Plan

- [x] Add top language jump labels to README files and localized quickstarts.
- [x] Rewrite the README first screen around what it does, who needs it, when to use it, and why to switch.
- [x] Update Chinese README with the same sharper positioning.
- [x] Update hero preview copy and regenerate the 2400x1400 image.
- [x] Run checks, commit, push, and verify GitHub rendering.

## Review Notes

- Keep the first screen concise: one-sentence purpose, use cases, reason to switch, then the HTML/JSON contract.
- Language links should stay as direct local links, not a separate docs system.
- Checks passed: examples, unit tests, markdown local links, `git diff --check`, hero image inspection, and GitHub metadata readback.

---

# Previous Task

Goal: tune naming and discovery terms for `html-artifact-report-skill`.

## Plan

- [x] Keep stable repo slug and skill id.
- [x] Shorten public name to `HTML Report Skill for AI Agents`.
- [x] Add natural search-entry terms: HTML artifact skill, agent report generator, Markdown-to-HTML report, JSON manifest report.
- [x] Update README, Chinese README, `llms.txt`, `SKILL.md`, install doc title, hero source, and GitHub metadata.
- [x] Run local checks and regenerate hero image.
- [x] Commit, push, and verify GitHub.

## Review Notes

- Do not rename the repository or skill id in this pass; current slug already captures `html`, `artifact`, `report`, and `skill`.
- Put query terms in the first screen and metadata, not as spammy keyword stuffing.
- Checks passed: examples, unit tests, markdown local links, `git diff --check`, generated hero image inspection, and GitHub metadata readback.

---

# Previous Task

Goal: polish the public GitHub packaging for `html-artifact-report-skill`.

## Plan

- [x] Read repository rules, README, SKILL, and Superpower instructions.
- [x] Review external packaging patterns and independent subagent feedback.
- [x] Replace README first screen with a stronger thesis and high-resolution hero.
- [x] Expand agent installation and first-run prompts for Claude Code, Codex, Cursor, Gemini CLI, DeepSeek-backed agents, and generic agents.
- [x] Add concise multilingual quickstarts.
- [x] Update `llms.txt` so agents can find the right entry points.
- [x] Run examples/tests, visual checks, and adversarial review.
- [x] Commit and push.

## Review Notes

- P1 from adversarial review: default `--agent '*' -g` install could fail for some clients and touch too many agent configs. Fixed by making per-agent install the default and verifying the Codex install command.
- P2 from adversarial review: duplicate Chinese quickstart source. Fixed by keeping `README.zh-CN.md` and deleting `docs/i18n/zh-CN.md`.
- P2 from adversarial review: Spanish/French localization lacked accents. Fixed link labels and quickstart text.
- P1 follow-up: Gemini CLI agent id was `gemini`, but `skills` expects `gemini-cli`. Fixed and verified with `npx skills ls -a gemini-cli --json`.
- Final checks passed: `scripts/check_examples.py`, `python3 -m unittest discover -s tests`, `git diff --check`, markdown local link check, and 2400x1400 hero image inspection.
