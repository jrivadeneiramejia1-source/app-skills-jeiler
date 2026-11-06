# app-skills-jeiler

Skills para que una aplicación quede bien hecha: **probarla, mejorar su interfaz y hacerla fluida**.
Es el hermano de `agent-skills-jeiler` (que es para agentes y automatizaciones).

Cada carpeta de `skills/` es una skill: un archivo `SKILL.md` con instrucciones para que Claude sepa cuándo y cómo usarla.

## Qué hay (37 skills)
| Grupo | Para qué |
|---|---|
| **A. Probar y verificar** | Comprobar que todo funciona, que no hay bugs y que no se puede romper fácil. |
| **B. Calidad web** | Accesibilidad, velocidad y buenas prácticas. |
| **C. Interfaz** | Que la app se vea bien y no parezca genérica. |
| **D. Fluidez** | Transiciones entre páginas y pantallas sin animaciones de adorno. |
| **E. PWA y calidad automática** | Apps instalables que abren sin internet, y revisión automática en GitHub Actions. |
| **F. Antes de construir** | Estudiar apps parecidas y elegir el diseño. |

La lista completa, con cuándo usar cada una y de dónde viene, está en **`INDICE-DE-SKILLS.md`**.

Las 6 skills originales de este repo son **`verificar-app`**, **`fluidez-interfaz`**, **`pwa-completa`**, **`ci-calidad-web`**, **`estudiar-app-referencia`** y **`elegir-diseno`** (licencia MIT, ver `LICENSE`). Las otras 31 son copias de repos con licencia libre; sus licencias están en `third-party/`.

## Cómo usarlas
Una skill solo funciona si está en la carpeta de skills de Claude (`~/.claude/skills/`). El instalador copia por grupos:

```bash
./instalar.sh --lista        # ver los grupos
./instalar.sh pruebas interfaz   # instalar esos grupos
```

**En sesiones en la nube** se instalan solos los grupos escritos en `grupos-activos.txt` (hoy: `pruebas`). Lo hace un hook de inicio en `.claude/`, y solo funciona si este repo está cargado como repo de la sesión. Edita ese archivo para cambiar los grupos.

El instalador no pisa una skill que ya exista con el mismo nombre y que no haya instalado él.

Mejor pocos grupos a la vez: cada skill agrega su descripción al contexto y eso gasta tokens.

## Revisor automático de PWA
```
python -I skills\pwa-completa\scripts\revisar_pwa.py CARPETA-DE-LA-WEB
```
Solo Python (igual en Windows y en la nube): revisa manifest, íconos, service worker, rutas, contenido `http://` y claves escritas, sin abrir un navegador. Salida 0 = sin graves, 1 = hay graves. Probado con una PWA buena, una mala hecha a propósito y 6 apps reales (ver `PRUEBAS.md`). **No prueba** que abra sin internet: eso se mira en un navegador en modo avión.

## Probar este repo
```
python -I -m unittest discover -s tests
```

## Qué falta o no está probado
- Probadas en tarea real: `verificar-app`, `fluidez-interfaz`, `pwa-completa`, `estudiar-app-referencia` y `elegir-diseno` (detalle y límites en `PRUEBAS.md`). `pwa-review` solo se probó en parte, y `ci-calidad-web` se probó en GitHub Actions con una copia de tu app. Del resto solo se verificó que los archivos son válidos y que no traen comandos de riesgo.
- `verificar-app` menciona `firebase-security-rules-auditor`, que vive en `agent-skills-jeiler`.
- Revisión de seguridad hecha con gitleaks: ver `SEGURIDAD.md`. Origen y versión de cada skill: ver `FUENTES.md`.
