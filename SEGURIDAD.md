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
