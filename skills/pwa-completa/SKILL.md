---
name: pwa-completa
description: Guía para construir una PWA (aplicación web instalable) completa, con manifest, íconos, service worker, que abra sin internet, datos guardados en el dispositivo, aviso de nueva versión e instalación en el teléfono. Usar cuando el usuario diga "que se instale como app", "que funcione sin internet", "que guarde los datos en el teléfono", "hacer la PWA" o antes de convertir una web en APK. Para auditar una PWA ya hecha usar la skill pwa-review.
---

# PWA completa

Una PWA es una web que se instala con icono, abre en pantalla completa y puede funcionar sin internet. Es el paso previo y más barato antes de pensar en un APK (ver `web-a-apk` en `apk-skills-jeiler`).

## Reglas
- Todo debe servirse por **HTTPS** (`localhost` está exceptuado para probar).
- **Los datos del usuario son suyos.** Si se guardan en el dispositivo, avisar que el navegador puede borrarlos y dar una forma de **exportar e importar** una copia.
- No guardar claves ni datos sensibles sin cifrar.
- Probar en un teléfono real; decir qué no se pudo probar.

## Qué debe tener
1. **`manifest.webmanifest`:** `name`, `short_name`, `start_url`, `display: standalone`, `theme_color`, `background_color` e íconos de 192 y 512 px, con una versión `maskable`.
2. **Rutas relativas.** En GitHub Pages la app vive en una subcarpeta (`/mi-app/`): una ruta que empieza con `/` se rompe. Poner el `scope` y la `start_url` relativos a la carpeta de la app.
3. **Service worker** (un archivo que intercepta las peticiones):
   - al instalarse, guarda en caché los archivos básicos de la app (HTML, CSS, JS, íconos);
   - archivos que casi no cambian: primero la caché;
   - datos que cambian: primero la red y, si falla, la caché;
   - una **página de respaldo** cuando no hay internet y el archivo no está guardado.
4. **Aviso de nueva versión.** Cuando haya un service worker nuevo, mostrar «Hay una versión nueva» con un botón para recargar. No forzar la recarga en medio de lo que el usuario está haciendo.
5. **Que el archivo del service worker no se guarde en caché por mucho tiempo** en el servidor (en Cloudflare, con un archivo `_headers`). Si se guarda por días, las actualizaciones tardan en llegar.
6. **Datos sin conexión:**
   - pocos datos y simples (ajustes, un contador): `localStorage`;
   - listas, textos largos o muchos registros: **IndexedDB**, con una librería pequeña que la envuelva;
   - pedir al navegador que no borre los datos (`navigator.storage.persist()`), sabiendo que puede negarse;
   - botón de **exportar e importar** (un archivo JSON).
7. **Instalación:**
   - Chrome en Android puede ofrecer un botón de instalar propio (evento `beforeinstallprompt`); hay que dejar también la opción manual del menú;
   - Safari en iPhone no tiene ese evento: mostrar una guía de «Agregar a pantalla de inicio».
8. **Avisos de seguridad:** no mezclar contenido por HTTP en una página por HTTPS; no guardar claves en el código del navegador.

## Revisor automático (antes de abrir un navegador)
Si la web está en una carpeta, correr (solo Python, sin instalar nada; no abre redes ni ejecuta la web):
```
python -I skills\pwa-completa\scripts\revisar_pwa.py CARPETA-DE-LA-WEB
```
Salida 0 = sin graves; 1 = hay ALTA; 2 = no encontró un `index.html`. Revisa el manifest (campos que Chrome exige, íconos que existan y midan lo que dicen), el service worker (que exista, responda a `fetch` y no precargue archivos inexistentes), rutas que se rompen en subcarpetas, contenido `http://`, datos sin exportar y claves escritas. Cada regla y su fuente: `references/reglas.md`. Ejemplos bueno y malo: `ejemplos/`. **No prueba** que abra sin internet: eso sigue siendo abrirla en un navegador en modo avión. Para publicar: `references/publicar-cloudflare-pages.md`.

## Medir en un navegador de verdad (antes de dar la PWA por buena)
`revisar_pwa.py` lee archivos; **`medir_pwa.mjs` abre la PWA en Chromium** (con Playwright), instala el service worker, **corta internet y recarga** para ver si de verdad abre:
```
node skills\pwa-completa\scripts\medir_pwa.mjs CARPETA-DE-LA-WEB
```
Necesita Node y Playwright (`npm install playwright`, Apache-2.0); opciones `--playwright-desde CARPETA` y `--chromium RUTA`. Levanta un servidor propio solo en `127.0.0.1`. Salida 0 = las 6 comprobaciones PASAN (service worker activo, caché con archivos, **abre sin internet con el mismo contenido**, manifest, íconos que cargan y miden lo que dicen, sin errores de consola); 1 = algo FALLA; 2 = no pudo medir. No prueba iPhone, Firefox ni el botón de instalar del navegador. Para ver la página por dentro (recursos cargados, cachés, claves de almacenamiento) con **REA**: `references/herramientas.md`.

## Proceso
1. Revisar qué tiene la app hoy (manifest, service worker, rutas, datos).
2. Hacer lo que falte, de la lista de arriba, **un punto a la vez**.
3. Probar sin internet: `medir_pwa.mjs` lo hace solo en Chromium; en el teléfono, modo avión y abrir desde el icono. Y con conexión lenta.
4. Auditar con la skill `pwa-review` (209 puntos, con evidencia; Lighthouse ya no tiene categoría de PWA desde la versión 12).
5. Pasar `verificar-app` antes de dar la app por terminada.
6. Si el usuario quiere APK: `web-a-apk`.

## Señales de alerta
- Rutas que funcionan en el computador y fallan al publicar.
- Una app que «abre sin internet» pero pierde lo que el usuario escribió.
- Un service worker que guarda todo para siempre y nunca se actualiza.
- Datos del usuario guardados sin forma de exportarlos.

## Verificación
- [ ] Se instala con icono y abre en pantalla completa.
- [ ] Abre sin internet y no pierde datos.
- [ ] Aparece el aviso de versión nueva al actualizar.
- [ ] Se puede exportar e importar una copia de los datos.
- [ ] Se auditó con `pwa-review` y se probó en un teléfono real.

## Qué se probó (2026-11-04 y 2026-11-06)
**Revisor automático (2026-11-06):** ejemplo bueno (0 hallazgos) y malo (22 hallazgos, 8 graves), más 20 pruebas con cambios puntuales, 4 PWA abiertas de MDN y 2 de la plantilla; el detalle y los falsos positivos que se corrigieron están en `PRUEBAS.md` y `references/reglas.md`.

**Primera prueba (2026-11-04):**
Se le pidió a un Claude aparte, con solo esta skill cargada, convertir una lista de tareas de un archivo en PWA. La abrió sola, tardó 11 turnos (unos 0,21 USD) y dejó manifest, íconos, `sw.js`, `_headers` y guardado en el aparato. Se revisó por fuera con un navegador automático: el service worker queda activo, el manifest y sus íconos responden, la tarea sigue tras recargar, **abre sin internet**, abre con datos guardados dañados, ofrece exportar e importar copia, sin errores de consola y sin desborde a 360 px. Lighthouse: 100 en rendimiento, accesibilidad y buenas prácticas, y 90 en SEO. No se probó en un teléfono real, ni la instalación con el botón del navegador, ni en iPhone.

