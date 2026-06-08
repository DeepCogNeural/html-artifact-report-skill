# HTML Artifact Report Skill - Démarrage rapide

<p>
  <a href="../../README.md"><kbd>English</kbd></a>
  <a href="../../README.zh-CN.md"><kbd>简体中文</kbd></a>
  <a href="es.md"><kbd>Español</kbd></a>
  <a href="ja.md"><kbd>日本語</kbd></a>
  <a href="fr.md"><kbd>Français</kbd></a>
</p>

Ce skill aide un agent à produire deux fichiers alignés:

- `artifact.html`: un rapport HTML autonome pour les lecteurs humains.
- `artifact.json`: un manifeste structuré pour les agents et l'automatisation.

Principe: HTML sert à la lisibilité; JSON sert à l'audit, aux preuves et à la réutilisation par les agents.

## Installation

```bash
npx skills add DeepCogNeural/html-artifact-report-skill \
  --agent codex \
  --skill html-artifact-report \
  -g -y
```

Remplacez `--agent codex` par `--agent claude-code`, `--agent cursor`, ou le client que vous utilisez.

## Premier prompt

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

## Règles

- Toujours produire les deux fichiers.
- `artifact.json` est un manifeste, pas un second rapport narratif.
- Les IDs de sections et de composants doivent correspondre entre HTML et JSON.
- Les fichiers locaux cités comme preuves doivent être présents dans `source_hashes`.
- La première vue doit donner la conclusion; les preuves longues doivent être repliées.
