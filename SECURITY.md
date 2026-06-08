# Security Policy

This repository does not execute untrusted report content. It provides templates, schemas, and static checker scripts.

## Report a vulnerability

Open a private security advisory on GitHub, or contact the repository owner through GitHub.

## Security expectations

- Do not add network execution to checker scripts.
- Do not add remote JavaScript dependencies to generated reports by default.
- Keep reports standalone unless a future contract explicitly allows external assets.
- Treat source hashes as integrity signals, not as a cryptographic trust boundary.

