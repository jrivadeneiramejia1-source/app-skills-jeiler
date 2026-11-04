# Qué se probó de verdad (2026-11-04)

Solo se listan las skills de este repo que se ejecutaron o se midieron. Las demás son copias de terceros y solo se revisó que sean válidas y seguras (ver `SEGURIDAD.md`).

| Skill | Estado | Qué se probó |
|---|---|---|
| **verificar-app** | Probada en tarea real | Se usó sobre la app `asesor-prompts` y encontró un fallo real (un doble toque en «Analizar» guarda dos entradas iguales). Trae `plantilla/ataque-web.mjs`, probada con 28 comprobaciones (27 bien, 1 fallo real). Se abrió sola en 1 de 3 frases de prueba (Sonnet 5.5); pedirla con su nombre asegura que se use. |
| **fluidez-interfaz** | Probada en tarea real | Se midió con `plantilla/medir-animaciones.mjs` sobre la misma app a 360 px: cambiar de pestaña termina a 260 ms (bien); analizar un borrador a 670 ms (pasa el tope de 400 ms por la entrada escalonada) y CLS 0,062. |
| **pwa-review** | Probada solo la recolección | `scripts/collect.py` corrió sobre la app real: bajó 18 archivos, escaneó 32 y detectó 32 señales de PWA. **No se hizo la puntuación completa de 209 puntos.** La prueba fue en local, sin HTTPS. |
| **elegir-diseno** | Solo se comprobó la fuente | La colección existe tal como dice: 84 carpetas, 84 `DESIGN.md`, de unos 24 KB cada uno (por eso la regla de leer solo 2 o 3). No se probó armando un `DESIGN.md` de principio a fin. |
| **estudiar-app-referencia** | Solo activación | Se abrió sola en 3 de 3 frases (Haiku). No se probó el proceso completo. |
| **pwa-completa** | Solo activación | Se abrió sola en 2 de 3 frases (Haiku). No se construyó una PWA con ella. |
| **ci-calidad-web** | Sin probar | Su flujo de GitHub Actions no se ha corrido. |

## Sobre la «activación sola»
Es si Claude abre la skill por su cuenta cuando el usuario pide algo parecido. Con 10 skills de los tres repos cargadas a la vez, en 50 frases (30 que debían activarla y 20 que no) con Haiku: **activó la correcta en 20 de 30 y nunca una equivocada (0 de 20)**. Son pocas repeticiones, con un modelo distinto al de uso diario; sirve como señal, no como medida exacta. La excepción clara es `verificar-app`: ante «ataca el código» o «rómpela con datos raros», el modelo se pone a trabajar sin abrirla (probé alargar su descripción y no cambió nada).

## Sin probar en ninguna skill
Teléfono real, otros navegadores distintos de Chromium, y nada que necesite claves de servicios externos.
