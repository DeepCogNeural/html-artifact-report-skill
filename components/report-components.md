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

Every major section should use `data-section-id`. Keep the heading compact: small numbered pill, H2, and a short muted intro below. Avoid heavy borders or large square number badges unless the report explicitly needs a dashboard look.

```html
<section data-section-id="decision">
  <div class="sec-head">
    <div class="num">01</div>
    <div>
      <h2>Decision</h2>
    </div>
  </div>
  <p class="sec-intro">One sentence explaining what this section proves.</p>
</section>
```

## 4. Decision Note Cards

Use when the report needs three plain-language buckets such as "adopt now / hold back / revisit later". Keep the card title serif and the body copy relaxed; these cards should read like editorial judgment, not a dashboard metric wall.

```html
<div class="decision-grid" data-component-id="cmp-decision-notes">
  <div class="note-card good">
    <h3>Adopt Now</h3>
    <p>Practices or changes that should become the default.</p>
  </div>
  <div class="note-card hot">
    <h3>Hold Back</h3>
    <p>Tempting options that would add risk before the evidence supports them.</p>
  </div>
  <div class="note-card">
    <h3>Revisit Later</h3>
    <p>Ideas worth tracking but not worth putting in the main path.</p>
  </div>
</div>
```

Use `.note-card.good` for green/olive adoption, `.note-card.hot` for clay warning, and plain `.note-card` for neutral future items.

## 5. Flow Visual

Use an inline SVG for simple flows. Use real labels. No decorative SVG characters or generic people illustrations.

```html
<div class="diagram" data-component-id="cmp-flow">
  <svg viewBox="0 0 760 160" role="img" aria-label="Artifact flow">
    <!-- report-specific SVG -->
  </svg>
</div>
```

## 6. Evidence Table

Short comparison tables may be visible. Long or raw tables must be folded in `<details>`.

```html
<div class="table-wrap" data-component-id="cmp-evidence-table">
  <table>
    <thead><tr><th>Check</th><th>Result</th><th>Meaning</th></tr></thead>
    <tbody><tr><td>Schema</td><td>Passed</td><td>JSON is valid</td></tr></tbody>
  </table>
</div>
```

## 7. Folded Evidence

Use for commands, logs, raw rows, long tables, and detailed source notes.

```html
<details data-component-id="cmp-raw-evidence">
  <summary>Raw evidence</summary>
  <pre>command output or source excerpt</pre>
</details>
```

## 8. Copyable Command

Use for reusable commands.

```html
<details data-component-id="cmp-commands">
  <summary>Reusable commands</summary>
  <button data-copy="#commands">Copy</button>
  <pre id="commands">python3 scripts/check_examples.py</pre>
</details>
```

## 9. Limitations

Limitations must be explicit when evidence is incomplete.

```html
<div class="card" data-component-id="cmp-limitations">
  <div class="k">Limitations</div>
  <p>One input was not independently verified.</p>
</div>
```

## Component selection guide

- decision, conclusion, recommendation -> TL;DR plus summary card
- adopt now / hold back / revisit later -> decision note cards
- ordered plan -> numbered sections
- process, dependency, data flow -> inline SVG diagram
- dense comparison -> table
- raw logs, long data, command output -> folded evidence
- reusable command -> copyable command
- unknowns, caveats, freshness gaps -> limitations card
