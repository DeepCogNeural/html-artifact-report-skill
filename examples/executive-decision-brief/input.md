# Adopt the HTML Artifact Report Skill

Decision needed: should the team publish v1 as a standalone skill repository?

Evidence:

- The v1 scope is limited to one report profile.
- The output contract has both `artifact.html` and `artifact.json`.
- The checker validates HTML structure, JSON schema, and ID alignment.

Risks:

- JSON and HTML can drift if IDs are not cross-checked.
- The README must avoid implying that upstream Apache-2.0 code was copied.

Recommendation: ship v1 as a clean-room MIT repository.

