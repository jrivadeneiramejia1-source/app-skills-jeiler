# Lecciones (errores aprendidos)

| Fecha | Qué pasó | Qué se aprendió |
|---|---|---|
| 2026-11-06 | `revisar_pwa.py` marcó `register('sw.js')` como archivo inexistente en una app real (`js/app.js` en una subcarpeta). | `register()` resuelve la ruta desde la **página**, no desde el `.js` que lo llama. Medir con apps reales destapa estas fallas. |
| 2026-11-06 | El mismo revisor marcó `/pwa-examples/a2hs/sw.js` como inexistente. | Una web puede publicarse bajo un prefijo: una ruta absoluta se prueba quitando carpetas del principio. |
| 2026-11-06 | Los enlaces `<a href="http://…">` se tomaron por contenido mixto. | Solo cuentan los recursos que se cargan (`script`, `link`, `img`, `iframe`…), no los enlaces. |
| 2026-11-06 | Claves de ejemplo dentro de `pruebas/` salían como graves. | En carpetas de pruebas baja a MEDIA («confirma que es inventado»); en lo que sirve la web sigue ALTA. |
| 2026-11-06 | La `description` de `pwa-completa` y de `ci-calidad-web` (skills propias) no era YAML válido por un «: » sin comillas. | Probar los encabezados con un lector de YAML de verdad (está en `tests/`). |
| 2026-11-06 | El repo no tenía `CLAUDE.md`. | Cada repo lleva las reglas de Jeiler en `CLAUDE.md`. |
| 2026-11-06 | `medir_pwa.mjs` leía el manifest **después** de cortar internet y encontraba la página de error del navegador en vez de la web. | Hacer todas las lecturas necesarias antes del paso que rompe el entorno (cortar internet). |
| 2026-11-06 | REA mostró `workers: []` aunque el service worker estaba activo. | Cada herramienta ve una parte: REA para recursos y almacenamiento, Playwright para el estado del service worker. Anotar el límite en vez de asumir. |
| 2026-11-06 | La predicción del revisor de texto (S04) se pudo **confirmar con el navegador**. | Cuando un revisor adivina un efecto («no se instalará»), hay que medirlo al menos una vez para saber que no es un falso aviso. |
| 2026-11-06 | `zizmor` marcaba la plantilla de calidad por usar `@v7` en vez de un commit fijo y por dejar las credenciales guardadas en `checkout`. | Las plantillas que se copian a otros proyectos deben pasar las herramientas de seguridad antes de entregarlas. |
