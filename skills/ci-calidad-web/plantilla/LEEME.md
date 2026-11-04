# Plantilla de calidad automática

Para una app web con `package.json` y `package-lock.json`.

## Instalar en un proyecto
1. Copiar `.github/workflows/calidad.yml` a la misma ruta del proyecto.
2. Copiar `lighthouserc.cjs` a la raíz del proyecto y ajustar `url`.
3. Instalar Lighthouse CI y agregar el script:
   ```bash
   npm install --save-dev @lhci/cli
   ```
   En `package.json`, dentro de `scripts`: `"lighthouse": "lhci autorun"`.
4. Revisar el paso «Pruebas del proyecto»: debe usar el comando de pruebas del proyecto (`npm test` u otro).
5. Subir los cambios en una rama, abrir un PR y mirar la pestaña **Actions**.

## Qué hace
| Trabajo | Qué comprueba | ¿Frena la publicación? |
|---|---|---|
| Pruebas | Corre las pruebas del proyecto | Sí, si fallan |
| Claves y dependencias | gitleaks busca claves escritas en el código; `npm audit` avisa de dependencias con fallos graves | gitleaks sí; `npm audit` solo avisa |
| Lighthouse | Mide velocidad, accesibilidad y buenas prácticas | No, solo avisa |

## Qué se probó
- El archivo del flujo pasa `actionlint` v1.7.12 (revisa la sintaxis de GitHub Actions).
- Los comandos de gitleaks (descarga, comprobación del checksum y escaneo) se corrieron en una carpeta local.
- Las versiones de `actions/checkout` y `actions/setup-node` y la configuración de Lighthouse están copiadas del flujo de `asesor-prompts`.
- **No se corrió este archivo en GitHub Actions.** La primera ejecución puede traer ajustes.
