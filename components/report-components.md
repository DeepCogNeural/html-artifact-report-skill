# Report Component Catalog

Use these components when creating `artifact.html`. Keep the structure simple and flat. Do not nest cards inside cards. Do not invent visual systems when a listed component fits.

Every meaningful component referenced by `artifact.json` needs a stable `data-component-id`.

## 1. TL;DR

Use once, immediately after the header.

```html
<div class="tldr" data-component-id="cmp-tldr">
  <strong>TL;DR:</strong> Decision first. Reason second. Risk third.
</div>
```

## 2. Summary Cards

Use for the top four signals a reader needs.

```html
<div class="summary" aria-label="summary" data-component-id="cmp-summary">
  <div class="card"><div class="k">Decision</div><div class="v">Proceed</div></div>
  <div class="card"><div class="k">Evidence</div><div class="v">4 checks</div></div>
  <div class="card"><div class="k">Risk</div><div class="v">Low</div></div>
  <div class="card"><div class="k">Next</div><div class="v">Ship v1</div></div>
</div>
```

## 3. Numbered Section Header

Every major section should use `data-section-id`.

```html
<section data-section-id="decision">
  <div class="sec-head">
    <div class="num">01</div>
    <div>
      <h2>Decision</h2>
      <p>One sentence explaining what this section proves.</p>
    </div>
  </div>
</section>
```

## 4. Flow Visual

Use an inline SVG for simple flows. Use real labels. No decorative SVG characters or generic people illustrations.

```html
<div class="diagram" data-component-id="cmp-flow">
  <svg viewBox="0 0 760 160" role="img" aria-label="Artifact flow">
    <!-- report-specific SVG -->
  </svg>
</div>
```

## 5. Evidence Table

Short comparison tables may be visible. Long or raw tables must be folded in `<details>`.

```html
<div class="table-wrap" data-component-id="cmp-evidence-table">
  <table>
    <thead><tr><th>Check</th><th>Result</th><th>Meaning</th></tr></thead>
    <tbody><tr><td>Schema</td><td>Passed</td><td>JSON is valid</td></tr></tbody>
  </table>
</div>
```

## 6. Folded Evidence

Use for commands, logs, raw rows, long tables, and detailed source notes.

```html
<details data-component-id="cmp-raw-evidence">
  <summary>Raw evidence</summary>
  <pre>command output or source excerpt</pre>
</details>
```

## 7. Copyable Command

Use for reusable commands.

```html
<details data-component-id="cmp-commands">
  <summary>Reusable commands</summary>
  <button data-copy="#commands">Copy</button>
  <pre id="commands">python3 scripts/check_examples.py</pre>
</details>
```

## 8. Limitations

Limitations must be explicit when evidence is incomplete.

```html
<div class="card" data-component-id="cmp-limitations">
  <div class="k">Limitations</div>
  <p>One input was not independently verified.</p>
</div>
```

## Component selection guide

- decision, conclusion, recommendation -> TL;DR plus summary card
- ordered plan -> numbered sections
- process, dependency, data flow -> inline SVG diagram
- dense comparison -> table
- raw logs, long data, command output -> folded evidence
- reusable command -> copyable command
- unknowns, caveats, freshness gaps -> limitations card

