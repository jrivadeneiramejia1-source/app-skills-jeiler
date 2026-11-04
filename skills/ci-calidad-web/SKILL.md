---
name: ci-calidad-web
description: Agrega a una app web un flujo de GitHub Actions que revisa la calidad solo en cada cambio: corre las pruebas, busca claves escritas en el código (gitleaks), avisa de dependencias con fallos graves y mide velocidad y accesibilidad con Lighthouse. Usar cuando el usuario diga "que se pruebe sola", "revisión automática", "que no se suban claves por error", "integración continua" o "Actions" para una app web.
---

# Calidad automática en GitHub Actions

La plantilla vive en `plantilla/` dentro de esta skill y se basa en el flujo de `asesor-prompts`. Instrucciones y alcance, en `plantilla/LEEME.md`.

## Reglas
- No subir ni activar nada sin que el usuario lo pida: los cambios van a una **rama** y a un PR, nunca directo a `main`.
- No pedir ni guardar claves. Si gitleaks encuentra una clave real, avisar sin copiarla y decir que hay que **cambiarla** (revocarla y crear otra), porque ya estuvo escrita en el historial.
- La plantilla se corrió en Actions una vez (ver `plantilla/LEEME.md`); en un proyecto nuevo, volver a revisar la pestaña Actions en la primera ejecución.

## Proceso
1. **Mirar el proyecto:** `package.json` (¿hay `npm test`?, ¿hay `package-lock.json`?), qué carpeta se publica y qué páginas conviene medir.
2. **Copiar la plantilla:** `calidad.yml` a `.github/workflows/`, `lighthouserc.cjs` a la raíz.
3. **Ajustar:** el comando de pruebas, las páginas (`url`) de Lighthouse y, si no hay `package-lock.json`, cambiar `npm ci` por `npm install`. Si las pruebas usan Playwright, dejar el paso «Navegador para las pruebas»; si no, borrarlo.
4. **Instalar Lighthouse CI** como dependencia de desarrollo y agregar el script `lighthouse`.
5. **Probar en local** lo que se pueda: `npm test`, y gitleaks sobre la carpeta (`gitleaks dir . --redact`).
6. **Validar la sintaxis** del flujo con `actionlint` si está disponible.
7. **Subir a una rama**, abrir un PR y revisar la pestaña Actions. Corregir lo que falle en la primera ejecución.
8. **Informe corto:** qué se agregó, qué se probó en local, qué falló en Actions y qué queda sin probar.

## Señales de alerta
- Un flujo que «pasa» porque no corre ninguna prueba de verdad.
- Una clave encontrada y solo «borrada» en un cambio nuevo: sigue en el historial; hay que cambiarla.
- Subir la plantilla directo a `main` sin mirar el resultado.

## Verificación
- [ ] El flujo pasa `actionlint` (o se dijo que no se pudo revisar).
- [ ] El comando de pruebas es el del proyecto.
- [ ] Se corrió en Actions desde un PR y se leyó el resultado.
- [ ] Ninguna clave quedó escrita en el flujo.
