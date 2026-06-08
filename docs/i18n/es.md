# HTML Artifact Report Skill - Inicio rápido

Este skill ayuda a un agente a crear dos archivos alineados:

- `artifact.html`: un informe HTML de un solo archivo para lectores humanos.
- `artifact.json`: un manifiesto estructurado para agentes y automatización.

La idea central: HTML mejora la lectura; JSON conserva estructura, evidencia y verificación para agentes futuros.

## Instalación

```bash
npx skills add DeepCogNeural/html-artifact-report-skill \
  --agent codex \
  --skill html-artifact-report \
  -g -y
```

Cambie `--agent codex` por `--agent claude-code`, `--agent cursor`, o el cliente que use.

## Primer prompt

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

## Reglas

- Siempre genere ambos archivos.
- `artifact.json` es un manifiesto, no otro ensayo.
- Los IDs de secciones y componentes deben coincidir entre HTML y JSON.
- Los archivos locales usados como evidencia deben aparecer en `source_hashes`.
- La primera pantalla debe dar la respuesta; la evidencia extensa debe estar plegada.
