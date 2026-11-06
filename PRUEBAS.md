# Qué se probó de verdad (2026-11-04)

Solo se listan las skills de este repo que se ejecutaron o se midieron. Las demás son copias de terceros y solo se revisó que sean válidas y seguras (ver `SEGURIDAD.md`).

| Skill | Estado | Qué se probó |
|---|---|---|
| **verificar-app** | Probada en tarea real | Se usó sobre la app `asesor-prompts` y encontró un fallo real (un doble toque en «Analizar» guarda dos entradas iguales). Trae `plantilla/ataque-web.mjs`, probada con 28 comprobaciones (27 bien, 1 fallo real). Se abrió sola en 1 de 3 frases de prueba (Sonnet 5.5); pedirla con su nombre asegura que se use. |
| **fluidez-interfaz** | Probada en tarea real | Se midió con `plantilla/medir-animaciones.mjs` sobre la misma app a 360 px: cambiar de pestaña termina a 260 ms (bien); analizar un borrador a 670 ms (pasa el tope de 400 ms por la entrada escalonada) y CLS 0,062. |
| **pwa-review** | Probada solo la recolección | `scripts/collect.py` corrió sobre la app real: bajó 18 archivos, escaneó 32 y detectó 32 señales de PWA. **No se hizo la puntuación completa de 209 puntos.** La prueba fue en local, sin HTTPS. |
| **elegir-diseno** | Probada en tarea real | Un Claude aparte eligió el diseño de una app de inventario y escribió un `DESIGN.md` propio. La colección existe (84 carpetas, unos 24 KB cada una). Se comprobó el contraste de sus 13 colores: todo pasa. No se probó construyendo una pantalla con él. |
| **estudiar-app-referencia** | Probada en tarea real | Un Claude aparte estudió apps de inventario de laboratorio y dejó una `ESPECIFICACION.md`. Las 4 licencias que citó se comprobaron y eran correctas. Estrellas y quejas de usuarios no se comprobaron. |
| **pwa-completa** | Probada en tarea real | Un Claude aparte, solo con esta skill, convirtió una lista de tareas en PWA. La revisión por fuera confirmó: abre sin internet, guarda y recupera datos, aguanta datos dañados, íconos y manifest bien, sin errores; Lighthouse 100/100/100/90 (SEO). No se probó en teléfono real ni en iPhone. |
| **ci-calidad-web** | Probada en GitHub Actions | Corrió en el repo de prueba `pantilla-apk` con una copia de `asesor-prompts`: los tres trabajos (pruebas con navegador, claves, Lighthouse) salieron bien. Antes, la comparación con el flujo de esa app encontró un hueco (faltaba instalar el navegador de Playwright) y se corrigió. Diferencias en la prueba: proyecto en subcarpeta y disparador por rama. |

## Revisor automático de PWA `revisar_pwa.py` (2026-11-06)
| Qué | Cómo | Resultado |
|---|---|---|
| PWA buena y PWA mala hechas a propósito | `pwa-completa/ejemplos/` | Buena: 0 hallazgos. Mala: 22 hallazgos (8 graves), salida 1. |
| 20 cambios puntuales sobre la PWA buena | quitar `viewport`, el enlace al manifest, `start_url`, `display`; ícono de 512 px o archivo de ícono ausente; ícono de otro tamaño; sin `maskable`; `start_url` con «/»; JSON roto; archivo de precarga inexistente; service worker ausente o sin `fetch`; comentarios que imitan código; clave en la web y en `pruebas/`… | Cada cambio dispara su regla. |
| Entradas rotas | carpeta inexistente, vacía, sin argumentos | Salida 2 con mensaje claro. |
| El informe no muestra valores | token inventado del ejemplo malo | No aparece. |
| **6 PWA reales** (2 de la plantilla y 4 de `mdn/pwa-examples`) | corridas completas | Primera pasada con **3 falsos positivos graves**: `register('sw.js')` desde un `.js` en subcarpeta, rutas absolutas bajo un prefijo (`/pwa-examples/a2hs/sw.js`) y enlaces `<a href="http://…">` tomados por contenido mixto; los tres corregidos y con prueba. Hoy quedan solo graves verdaderos (`a2hs`: ícono de 512 px y `viewport` ausentes; `cycletracker`: manifest sin enlazar). |
| Pruebas del repo (`tests/`) | `python -I -m unittest discover -s tests`: grupos, encabezados YAML, `python` y no `python3`, sin correos reales, revisor | 29 pruebas, todas pasan. |
| Las pruebas detectan fallas | Se rompió a propósito la regla de la lista de precarga y la del `viewport` | En cada caso fallaron 2 pruebas (bien); se restauró. |
| Errores en skills propias que encontraron las pruebas de encabezado | `pwa-completa` y `ci-calidad-web` tenían una `description` que un lector de YAML estricto rechaza («completa: manifest…», «cambio: corre…») | Corregidas sin cambiar el sentido. |

**No probado:** que una PWA realmente abra sin internet (el revisor no ejecuta JavaScript); la publicación en Cloudflare Pages (la guía sale de su documentación oficial, no de haberla hecho); teléfono real.

## Arranque automático (hook) — probado el 2026-11-04
Se abrió una sesión nueva en la nube con este repo (rama de trabajo) y, sin hacer nada, `~/.claude/skills` ya tenía las **12 skills del grupo `pruebas`**, todas con la marca del instalador, incluida `verificar-app`. Es decir, el hook de inicio funciona. Solo se probó con este repo; los de `agent-skills-jeiler` y `apk-skills-jeiler` usan el mismo mecanismo pero no se abrieron en una sesión propia. Esa prueba costó unos 0,12 USD.

## Sobre la «activación sola»
Es si Claude abre la skill por su cuenta cuando el usuario pide algo parecido. Con 10 skills de los tres repos cargadas a la vez, en 50 frases (30 que debían activarla y 20 que no) con Haiku: **activó la correcta en 20 de 30 y nunca una equivocada (0 de 20)**. Son pocas repeticiones, con un modelo distinto al de uso diario; sirve como señal, no como medida exacta. La excepción clara es `verificar-app`: ante «ataca el código» o «rómpela con datos raros», el modelo se pone a trabajar sin abrirla (probé alargar su descripción y no cambió nada).

## Sin probar en ninguna skill
Teléfono real, otros navegadores distintos de Chromium, y nada que necesite claves de servicios externos.
