# app-skills-jeiler

Skills para que una aplicación quede bien hecha: **probarla, mejorar su interfaz y hacerla fluida**.
Es el hermano de `agent-skills-jeiler` (que es para agentes y automatizaciones).

Cada carpeta de `skills/` es una skill: un archivo `SKILL.md` con instrucciones para que Claude sepa cuándo y cómo usarla.

## Qué hay (32 skills)
| Grupo | Para qué |
|---|---|
| **A. Probar y verificar** | Comprobar que todo funciona, que no hay bugs y que no se puede romper fácil. |
| **B. Calidad web** | Accesibilidad, velocidad y buenas prácticas. |
| **C. Interfaz** | Que la app se vea bien y no parezca genérica. |
| **D. Fluidez** | Transiciones entre páginas y pantallas sin animaciones de adorno. |

La lista completa, con cuándo usar cada una y de dónde viene, está en **`INDICE-DE-SKILLS.md`**.

Las dos skills que son originales de este repo: **`verificar-app`** y **`fluidez-interfaz`**. Las otras 30 son copias de repos con licencia libre; sus licencias están en `third-party/`.

## Cómo usarlas
Una skill solo funciona si está en la carpeta de skills de Claude (`~/.claude/skills/`). Copia solo las que necesites:

```bash
cp -r skills/verificar-app ~/.claude/skills/
```

Mejor cargar por grupos y no todas a la vez: cada skill agrega su descripción al contexto y eso gasta tokens.

## Qué falta o no está probado
- Ninguna skill se ha probado en una tarea real; solo se verificó que los archivos son válidos y que no traen comandos de riesgo.
- `verificar-app` menciona `firebase-security-rules-auditor`, que vive en `agent-skills-jeiler`.
