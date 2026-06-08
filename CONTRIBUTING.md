# Contributing

This project is intentionally small. Contributions should make the one canonical report skill more reliable, not turn it into a general app or template platform.

## Good contributions

- Better checker coverage.
- Better negative fixtures.
- Clearer contract wording.
- Stronger examples.
- Bug fixes in HTML/JSON alignment.
- Accessibility or print-readability improvements that preserve the canonical profile.

## Out of scope for v1

- GUI app.
- Live preview server.
- PNG or social-card export.
- Markdown/docx/html conversion pipelines.
- Large template catalogs.
- Default sidebar table of contents.

## Required checks

Run:

```bash
python3 scripts/check_examples.py
python3 -m unittest discover -s tests
```

When changing checker behavior, add or update a negative fixture so CI proves the failure mode is covered.

