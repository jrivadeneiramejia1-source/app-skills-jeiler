# Lecciones (errores aprendidos)

| Fecha | Qué pasó | Qué se aprendió |
|---|---|---|
| 2026-11-06 | `revisar_pwa.py` marcó `register('sw.js')` como archivo inexistente en una app real (`js/app.js` en una subcarpeta). | `register()` resuelve la ruta desde la **página**, no desde el `.js` que lo llama. Medir con apps reales destapa estas fallas. |
| 2026-11-06 | El mismo revisor marcó `/pwa-examples/a2hs/sw.js` como inexistente. | Una web puede publicarse bajo un prefijo: una ruta absoluta se prueba quitando carpetas del principio. |
| 2026-11-06 | Los enlaces `<a href="http://…">` se tomaron por contenido mixto. | Solo cuentan los recursos que se cargan (`script`, `link`, `img`, `iframe`…), no los enlaces. |
| 2026-11-06 | Claves de ejemplo dentro de `pruebas/` salían como graves. | En carpetas de pruebas baja a MEDIA («confirma que es inventado»); en lo que sirve la web sigue ALTA. |
| 2026-11-06 | La `description` de `pwa-completa` y de `ci-calidad-web` (skills propias) no era YAML válido por un «: » sin comillas. | Probar los encabezados con un lector de YAML de verdad (está en `tests/`). |
| 2026-11-06 | El repo no tenía `CLAUDE.md`. | Cada repo lleva las reglas de Jeiler en `CLAUDE.md`. |
