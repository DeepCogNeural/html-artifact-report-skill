# Artifact Contract Design Review

Goal: prevent drift between a human HTML report and an agent-readable JSON manifest.

Design:

1. Generate a semantic outline.
2. Write `artifact.json` from the outline.
3. Render `artifact.html` with matching section and component IDs.
4. Run schema validation and HTML/JSON cross-checks.

Main risk: a report can look right while the manifest points to stale IDs.

Decision: make ID alignment a required checker.

