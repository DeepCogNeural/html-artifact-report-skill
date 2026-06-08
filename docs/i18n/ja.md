# HTML Artifact Report Skill クイックスタート

<p>
  <a href="../../README.md"><kbd>English</kbd></a>
  <a href="../../README.zh-CN.md"><kbd>简体中文</kbd></a>
  <a href="es.md"><kbd>Español</kbd></a>
  <a href="ja.md"><kbd>日本語</kbd></a>
  <a href="fr.md"><kbd>Français</kbd></a>
</p>

この skill は、agent が次の 2 つのファイルを同時に作るためのものです。

- `artifact.html`: 人が読むための単一ファイル HTML レポート。
- `artifact.json`: agent と自動処理が検証するための構造化 manifest。

基本方針: HTML は読みやすさを担当し、JSON は構造、根拠、検証結果を保存します。

## インストール

```bash
npx skills add DeepCogNeural/html-artifact-report-skill \
  --agent codex \
  --skill html-artifact-report \
  -g -y
```

Claude Code で使う場合は `--agent codex` を `--agent claude-code` に変更してください。Cursor など他のクライアントでも同じ考え方です。

## 最初のプロンプト

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

## ルール

- 必ず `artifact.html` と `artifact.json` の両方を作成する。
- `artifact.json` は別の文章レポートではなく、manifest として使う。
- HTML と JSON の section/component ID は完全に一致させる。
- ローカル evidence ファイルは `source_hashes` に入れる。
- 最初の画面で結論を示し、長い証拠は折りたたむ。
