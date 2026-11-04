---
name: elegir-diseno
description: Ayuda a elegir y armar el diseño de una app partiendo de sistemas de diseño ya probados (colección de 84 archivos DESIGN.md de sitios reales). Compara 2 o 3 opciones, extrae principios (colores, letras, espacios) y escribe un DESIGN.md propio para el proyecto, cuidando contraste y accesibilidad. Usar cuando el usuario diga "no sé qué diseño ponerle", "que se vea como una app profesional", "ayúdame a elegir colores y letras" o al empezar una app nueva.
---

# Elegir el diseño de una app

La colección es `VoltAgent/awesome-design-md` (tu fork: `awesome-design-jeiler`, licencia MIT): 84 carpetas, cada una con un `DESIGN.md` que describe cómo está diseñado un sitio real (colores, letras, espacios, componentes). Cada archivo tiene varios cientos de líneas (el de Airbnb, 545) y secciones como *Overview*, *Colors*, *Typography* y *Layout*.

## Reglas
- **Inspirarse, no imitar marcas.** Tomar principios (jerarquía, espacios, ritmo, tipo de letra) y construir un diseño propio. No copiar logos, nombres, íconos, textos ni la combinación exacta de colores de una empresa.
- La app debe cumplir **contraste suficiente** y botones táctiles de 44 px o más.
- No pedir ni guardar claves.
- No leer los 84 archivos: son largos y gastan tokens. Elegir 2 o 3.

## Proceso
1. **Preguntar** (una sola vez, con opciones): para qué es la app, quién la usa, qué sensación debe dar (seria, cálida, juguetona, minimalista) y si tiene colores o logo ya definidos.
2. **Obtener la colección:** `git clone --depth 1 https://github.com/VoltAgent/awesome-design-md` en una carpeta aparte (no dentro del repo del usuario). Listar los nombres de `design-md/` y elegir **2 o 3** que encajen.
3. **Leer solo** *Overview*, *Colors*, *Typography* y *Layout* de cada una.
4. **Comparar** en una tabla corta: sensación, colores principales, familia de letra, escala de espacios.
5. **Proponer** una dirección (la más simple que sirva) y mostrar por qué.
6. **Escribir un `DESIGN.md` propio** para el proyecto, con: paleta (con usos), tipografía (con tamaños), escala de espacios, forma de botones y campos, y tres reglas de uso. El usuario ya usa este formato en `asesor-prompts` y `apps-consulta-previa`.
7. **Comprobar el contraste** del texto sobre cada fondo (relación mínima 4,5:1 para texto normal). Usar la skill `accessibility` o una calculadora de contraste.
8. **Aplicarlo** con `ui-ux-pro-max`, `design-system` o `frontend-design`, y revisar el resultado con `verificar-app`.

## Señales de alerta
- Un diseño que parece una copia de una marca conocida.
- Texto gris claro sobre fondo blanco que no se lee al sol.
- Más de 2 familias de letra o más de 5 colores sin un uso definido.
- Leer los 84 archivos «por si acaso».

## Verificación
- [ ] Se compararon 2 o 3 opciones, no una sola.
- [ ] El `DESIGN.md` propio no copia colores, nombres ni logos de una marca.
- [ ] El contraste del texto cumple 4,5:1.
- [ ] Los botones táctiles miden 44 px o más.
