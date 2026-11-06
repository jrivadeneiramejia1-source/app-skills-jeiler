# Revisión de seguridad

Hecha el 2026-11-04.

## Qué se revisó y cómo
1. **gitleaks 8.30.0** (busca claves y tokens escritos en archivos). Se descargó del sitio oficial y se verificó su checksum (`OK`). Se corrió sobre los archivos actuales y sobre todo el historial de git.
2. **Búsqueda propia de comandos de riesgo** en los scripts de las skills copiadas: descargar y ejecutar a la vez (`curl ... | sh`), `eval`, `rm -rf /`, `base64 -d`, `nc -e`, `sudo`.
3. **No se ejecutó `snyk/agent-scan`.** Pide crear una cuenta en Snyk y un token, y envía el contenido de las skills a su servicio. No lo usé por eso. Queda pendiente si decides crear la cuenta tú.

## Resultado
- **gitleaks:** 0 hallazgos en los archivos actuales y en el historial.
- **Comandos de riesgo:** ninguno en los scripts de las 32 skills.
- Algunas skills traen scripts (31 archivos `.sh`, `.py` y `.mjs`, entre ellos los de `ui-ux-pro-max` y `webapp-testing`). Revisé solo las señales de la lista de arriba, no el código completo.

## Fase 3 (skills nuevas, 2026-11-04)
- Se agregó 1 skill de terceros (`pwa-review`) y 4 originales. La búsqueda de comandos de riesgo salió vacía; gitleaks sin hallazgos.
- `pwa-review` trae un script, `scripts/collect.py` (750 líneas, solo biblioteca estándar de Python). Lo leí: descarga la página que se audita y sus archivos (máximo 80 peticiones y 5 MB cada una) y los guarda en la carpeta de salida; no usa `subprocess`, `eval` ni `exec`. Se probó en modo «solo código» sobre `asesor-prompts`. Del repo de origen se quitaron `tests/`, `README.md` y `CHANGELOG.md` para no cargar peso.
- La plantilla `ci-calidad-web` descarga gitleaks y comprueba su checksum antes de usarlo. No se ha corrido en GitHub Actions.
- `estudiar-app-referencia` y `elegir-diseno` piden descargar repos de terceros en una carpeta aparte. No se copia nada de ellos a este repo.

## Fase 7 (2026-11-06)
- Se agregó `pwa-completa/scripts/revisar_pwa.py` (original, solo Python estándar): solo lee archivos y tamaños de íconos PNG; no abre redes, no ejecuta el JavaScript de la web y no imprime valores de claves. Sin código de terceros nuevo.
- **gitleaks 8.30.0** (descargado del sitio oficial, checksum `OK`) sobre los archivos: **0 hallazgos**.
- El ejemplo malo (`pwa-mala`) trae un token inventado a propósito.
- Se agregó `CLAUDE.md` con las reglas de Jeiler.

## Fase 8 (2026-11-06, segunda ronda)
- `medir_pwa.mjs` (original): levanta un servidor **solo en 127.0.0.1** y en un puerto libre, no deja salir peticiones a otros sitios que no pida la propia web, y no guarda nada. Usa Playwright (Apache-2.0) del entorno.
- REA 6.5.0 (MIT) se construyó en una copia temporal y se usó de forma pasiva sobre páginas propias; el repo `rea.-` no se modificó.
- actionlint 1.7.12 y zizmor 1.32.0 (MIT) se usaron sin copiarlos (ver `skills/pwa-completa/references/herramientas.md`).
- Las acciones de la plantilla `ci-calidad-web` ahora van fijadas a un commit, con `persist-credentials: false`.
- **gitleaks sobre el historial completo** (13 commits): 0 hallazgos.
