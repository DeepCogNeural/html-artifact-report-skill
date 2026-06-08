# HTML Report Skill for AI Agents

给人看的 HTML artifact，给 agent 看的 JSON manifest。

这个仓库提供一个可复用 agent skill：把重要笔记、Markdown、研究、设计评审、决策 memo 转成两份对齐的文件：

- `artifact.html`：暖色 editorial 风格的单文件 HTML 报告，方便人读。
- `artifact.json`：结构化 manifest，方便 agent 复查、diff、复用。
- checker 会强制 HTML 的 `data-section-id` / `data-component-id` 和 JSON contract 对齐。

不同用户可能会搜：HTML report skill、HTML artifact skill、agent report generator、Markdown-to-HTML report、JSON manifest report。这里都指向同一个 contract。

## 安装

选择你正在用的 agent，只安装到那个客户端。

Claude Code：

```bash
npx skills add DeepCogNeural/html-artifact-report-skill \
  --agent claude-code \
  --skill html-artifact-report \
  -g -y
```

Codex：

```bash
npx skills add DeepCogNeural/html-artifact-report-skill \
  --agent codex \
  --skill html-artifact-report \
  -g -y
```

如果不想安装，可以生成一次性提示词：

```bash
npx skills use DeepCogNeural/html-artifact-report-skill@html-artifact-report
```

## 第一次使用

```text
Use html-artifact-report.
Read SKILL.md, SPEC.md, templates/desktop-report-template.html,
components/report-components.md, and one complete example first.

Input: notes.md
Output:
- artifact.html
- artifact.json

Run:
python3 scripts/check_html_artifact.py artifact.html
python3 scripts/check_artifact_json.py artifact.json --html artifact.html
```

## 核心规则

- 不要只生成 HTML，必须同时生成 JSON。
- JSON 不是第二篇报告，而是 manifest。
- HTML 和 JSON 的 section/component ID 必须完全对齐。
- 本地 evidence 文件必须写入 `source_hashes`。
- 首屏先给结论，长证据折叠。

更多 agent 安装方式见 [docs/agents.md](docs/agents.md)。
