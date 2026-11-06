# Herramientas para medir una PWA

Marcas: **[F]** fuente abierta citada · **[P]** regla práctica sin verificar · **[E]** hecha y medida aquí. Consultado el 2026-11-06.
Ninguna se copia a este repo.

| Herramienta | Versión | Licencia | Para qué |
|---|---|---|---|
| Playwright | la instalada en el entorno | Apache-2.0 | Abrir Chromium, controlar la red y leer el estado del service worker (`medir_pwa.mjs`) |
| REA (tu fork `rea.-`) | 6.5.0 | MIT | Mirar la página por dentro de forma pasiva |
| actionlint / zizmor | 1.7.12 / 1.32.0 | MIT / MIT | Revisar los flujos de GitHub Actions (plantilla en `ci-calidad-web/plantilla`) |
| Lighthouse | — | Apache-2.0 | Rendimiento, accesibilidad y SEO (ya no tiene categoría de PWA desde la versión 12, ver `pwa-completa`) |

## Comprobación cruzada: lo que predice el revisor, lo que pasa de verdad [E]
Se sirvieron `ejemplos/pwa-buena` y `ejemplos/pwa-mala` en `127.0.0.1` y se midió en Chromium:
| | Revisor de texto (`revisar_pwa.py`) | Navegador (`medir_pwa.mjs`, Playwright) | REA (`inspect-web-page`) |
|---|---|---|---|
| pwa-buena | 0 hallazgos | 6 de 6: service worker activo, caché `tareas-v1` con 7 archivos, **abre sin internet** | caché `tareas-v1`, 11.108 bytes de uso, manifest cargado como recurso |
| pwa-mala | 22 hallazgos (S04: la precarga incluye un archivo que no existe) | 1 de 6: **el service worker nunca se instala**; caché `v1` creada pero **vacía** (`addAll` falló); no abre sin internet; ícono que mide 100x100 y dice 192; 404 de `/img/logo.png`; falla la hoja de estilos por `http://` | caché `v1` con **0 bytes de uso**; clave `x` en `localStorage` (la que la regla D01 sospechaba) |
La predicción S04 («el service worker no se instalará») **se confirmó en el navegador**.
- `pantilla-apk/www`, `asesor-calidad` (apps reales) y la web **dentro del APK** de la plantilla: 6 de 6, abren sin internet.
- `mdn/pwa-examples/a2hs` servida desde la raíz: el service worker falla (404) porque su `register` usa una ruta con prefijo (`/pwa-examples/a2hs/sw.js`); el revisor de texto no lo marca como grave a propósito (no puede saber bajo qué carpeta se publica) pero sí avisa de `start_url` absoluta (M09).

## REA sobre una página [E]
1. Construir REA en una **copia** (no modificar el repo): `npm ci --ignore-scripts && npm run build:cached` (Node 22; unos 3 minutos).
2. Abrir **una sola** página con Chromium propio: `chromium --headless=new --no-sandbox --disable-gpu --disable-dev-shm-usage --remote-debugging-port=9333 --user-data-dir=CARPETA-TEMPORAL URL` (con más de una URL falla: «Multiple targets are not supported in headless mode»; la segunda se abre con `curl -X PUT "http://127.0.0.1:9333/json/new?URL"`).
3. `node scripts/rea.mjs list-browser-targets http://127.0.0.1:9333` y luego `inspect-web-page http://127.0.0.1:9333 ID-DEL-OBJETIVO --observation-ms 2500 --include-storage-keys --include-console-text`.
- Qué entrega: scripts y recursos cargados (con tipo `Manifest`), nombres de cachés y bytes de uso, claves de `localStorage` (sin valores), consola y red de la ventana observada.
- **Límite medido:** en `workers` salió vacío incluso con el service worker activo; para el estado del service worker usar `medir_pwa.mjs`.
- REA se usa solo sobre páginas tuyas o de código abierto, de forma pasiva.

## Plantillas de flujos [E]
`ci-calidad-web/plantilla/.github/workflows/calidad.yml`: antes zizmor daba **5 `unpinned-uses` y 3 `artipacked`** (actionlint 0). Ahora las acciones van fijadas a su commit y `checkout` lleva `persist-credentials: false`: **0** con ambos. **No se volvió a correr en Actions** (la versión anterior sí se probó en `pantilla-apk`). Nueva `revisar-flujos.yml` (misma de `verificar-apk` en `apk-skills-jeiler`).
