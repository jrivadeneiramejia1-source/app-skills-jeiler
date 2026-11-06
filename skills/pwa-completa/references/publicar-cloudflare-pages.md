# Publicar una web estática (PWA) en Cloudflare Pages

Marcas: **[F]** fuente abierta citada · **[P]** regla práctica sin verificar · **[E]** hecha y medida aquí.
Fuentes consultadas el 2026-11-06 (ver `fuentes.md`).

## Pasos con Git (sin compilar nada) [F]
1. La web (con `index.html`, `manifest.webmanifest`, `sw.js`, íconos) va en un repositorio de GitHub, en la rama `main`.
2. En el panel de Cloudflare: Workers & Pages → Create application → pestaña **Pages** → «Import an existing Git repository» y se elige el repo.
3. Rama de producción: `main`. **Build command (comando de construcción): `exit 0`** si no hay nada que compilar (Cloudflare lo recomienda para activar Pages Functions). **Build output directory: la carpeta que contiene `index.html`** (si está en la raíz, se deja vacío o con `/`; confirmar en el panel).
4. Se publica en una dirección `*.pages.dev`; cada subida a `main` vuelve a publicar y cada pull request tiene una vista previa.
- «Direct Upload» (subir la carpeta con `wrangler pages deploy`) existe, pero esa página no lo explica y **no lo verifiqué**: ver la guía «Get started» de Pages.

## El archivo `_headers` (para que `sw.js` se actualice) [F]
Va en la carpeta que se publica, se llama `_headers` (sin extensión) y no se sirve como archivo; Cloudflare lo interpreta. Formato: una ruta, y debajo, con sangría, un encabezado por línea; los comentarios empiezan con `#`.
```
/sw.js
  Cache-Control: no-cache
```
- Límites: hasta **100 reglas**; cada línea, máximo **2.000 caracteres**. Si un encabezado se define dos veces, los valores se unen con comas.
- **No se aplica a respuestas de Pages Functions** (solo a archivos estáticos).
- Por qué importa para una PWA **[P]**: si el navegador guarda `sw.js` por mucho tiempo, las versiones nuevas tardan en llegar. El revisor `revisar_pwa.py` avisa (S08) si no ve esta regla.

## Límites del plan gratis [F]
- 500 builds al mes y 1 build a la vez.
- Hasta 20.000 archivos por sitio y 25 MiB por archivo.
- 100 proyectos por cuenta y 100 dominios personalizados por proyecto.
- Para una web estática con `exit 0` casi no gastas builds, pero cada subida a `main` cuenta uno **[P]**.

## Pages o Workers [F]
Cloudflare compara ambos en su guía de migración: Workers (con «static assets») tiene un conjunto de funciones más amplio que Pages. **No encontré que Pages esté descontinuado** ni una fecha de fin de soporte. Para una web estática simple, Pages sigue sirviendo; si necesitas funciones nuevas de Cloudflare, mira la guía de migración.

## Antes de publicar [E]
Correr `python -I skills\pwa-completa\scripts\revisar_pwa.py CARPETA-DE-LA-WEB`: salida 0 y sin ALTA. Después, abrir la dirección `*.pages.dev` en un navegador, instalar la app y probar en modo avión.

## No probado aquí
No publiqué nada en Cloudflare Pages (no tengo tus cuentas ni claves). Los pasos salen de la documentación oficial, no de haberlos hecho.
