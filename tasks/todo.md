# Current Task

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
