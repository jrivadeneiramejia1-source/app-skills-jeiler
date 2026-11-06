# Reglas del revisor `revisar_pwa.py`

Marcas: **[F]** fuente abierta citada · **[P]** regla práctica sin verificar · **[E]** hecha y medida aquí.

| Id | Gravedad | Regla | Marca | Base |
|---|---|---|---|---|
| P01 M01 | ALTA | El manifest debe existir, ser JSON válido y estar enlazado con `<link rel="manifest">`. | [F] | web.dev, «Installability criteria». |
| M02 M03 M04 | ALTA | `name` o `short_name`, `start_url` y `display` (`standalone`, `fullscreen`, `minimal-ui` o `window-controls-overlay`). | [F] | Misma página. |
| M05 | ALTA/MEDIA | Íconos de 192 y 512 px que existan en disco y midan lo que dice el manifest. | [F]/[P] | Los tamaños: web.dev. Que midan lo declarado: regla práctica (el revisor lee el encabezado del PNG). |
| M08 | ALTA | `prefer_related_applications` en true impide instalar. | [F] | Misma página. |
| M06 | MEDIA | Un ícono `maskable`. | [P] | En Android sin él el ícono puede recortarse. No verificado en fuente. |
| M07 P04 | BAJA | Colores del tema. | [P] | |
| M09 P08 | MEDIA | Rutas que empiezan con «/» se rompen si la app vive en una subcarpeta (GitHub Pages). | [E] | Visto en la skill `pwa-completa` y al medir con apps reales (MDN publica bajo `/pwa-examples/…`). |
| P02 | ALTA | `<meta name="viewport">`. | [P] | Sin él el teléfono dibuja la página de escritorio. |
| P03 P05 P06 | MEDIA | `lang`, `<title>`, `alt` en imágenes. | [P] | Accesibilidad básica. |
| P07 | ALTA/MEDIA | Recursos cargados por `http://` (script y CSS: ALTA). No cuenta `<a href>`. | [E] | El primer intento marcaba enlaces `<a href="http://…">` (falso positivo en MDN); corregido. |
| S01 S03 | MEDIA | Debe haber `serviceWorker.register` y el service worker debe responder a `fetch`. | [P] | Sin eso la app no abre sin internet (el instalador de Chrome no lo exige: ver fuentes). |
| S02 | ALTA | El archivo del service worker debe existir. La ruta se resuelve desde la página, no desde el `.js` que llama a `register`. | [E] | Falso positivo real en `asesor-calidad` (el `js/app.js` registraba `sw.js`). |
| S04 | ALTA | Todo archivo de la lista de precarga (`addAll`) debe existir. | [P] | Si falta uno, `cache.addAll` falla y el service worker no se instala. |
| S05 | MEDIA | Borrar cachés viejas (`caches.delete`). | [P] | |
| S08 | BAJA | Que `sw.js` no se guarde por días (`_headers` en Cloudflare Pages). | [F]/[P] | Formato de `_headers`: Cloudflare. Por qué importa: regla práctica. |
| D01 | BAJA | Si guarda datos en el aparato, ofrecer exportarlos. | [P] | `pwa-completa`, regla de datos del usuario. |
| K01 | ALTA (MEDIA en carpetas de pruebas) | Claves escritas en archivos de la web. | [P] | Cualquiera puede leer lo que sirve la web. |

## Medido aquí [E]
- `pantilla-apk/www` (PWA mínima): 0 graves; 1 aviso bajo (S08, sin `_headers`).
- `pantilla-apk/proyectos/asesor-calidad` (app real): 0 graves; 6 avisos medios, todos de la regla K01 en `pruebas/` (valores inventados para probar un detector de claves).
- `mdn/pwa-examples` (4 apps): las primeras pasadas dieron falsos graves (rutas con prefijo, `<a href>`, ruta del service worker). Corregidos. Quedan graves **verdaderos**: `a2hs` solo declara un ícono de 192 px y no tiene `viewport`; `cycletracker` no enlaza el manifest en la página raíz.

## Límites
- No ejecuta JavaScript ni abre un navegador: no prueba que abra sin internet ni que el service worker se instale.
- La lista de precarga solo se lee si es un arreglo de textos escrito en el archivo (o una constante).
- Para auditar a fondo, `pwa-review` (209 puntos).
