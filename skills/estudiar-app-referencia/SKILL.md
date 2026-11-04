---
name: estudiar-app-referencia
description: Antes de construir una app, estudia 3 a 5 apps parecidas (preferiblemente de código abierto) para saber qué funciones tienen, cómo se ven, qué errores comunes tuvieron y qué licencia permite copiar. Termina con una especificación corta para construir la app propia. Usar cuando el usuario diga "quiero hacer una app que haga esto", "hay alguna app parecida", "no quiero empezar de cero", "hazle ingeniería inversa a una app" o "qué hicieron bien y mal otras apps".
---

# Estudiar apps de referencia

Objetivo: no empezar de cero y no repetir errores que otros ya cometieron. Se aprende de apps existentes **sin copiar lo que no se puede copiar**.

## Reglas
- **Licencia primero.** Antes de leer código para reutilizarlo, mirar la licencia:
  - MIT, Apache-2.0, BSD o CC0: se puede reutilizar código con atribución (guardar el aviso de licencia).
  - GPL o AGPL: solo estudiar las ideas. **No copiar su código** a una app con otra licencia.
  - Sin licencia: no copiar nada; solo estudiar el comportamiento.
- **Apps de código cerrado:** solo mirar lo que cualquiera ve (funciones, pantallas, descripción en la tienda). **No descompilar APKs ni copiar código, imágenes, textos o marcas.** Puede violar derechos de autor y las reglas de las tiendas.
- No pedir ni guardar claves. No iniciar sesión en servicios ajenos.
- Decir qué no se pudo ver.

## Proceso
1. **Definir la app en 3 líneas:** qué hace, para quién y en qué dispositivo (teléfono, computador, ambos).
2. **Buscar 3 a 5 apps parecidas.** En GitHub (funciona sin acceso al repo):
   ```bash
   gh api -X GET search/repositories -f q="<tema> <lenguaje o tipo>" -f sort=stars -f per_page=10 \
     --jq '.items[] | "\(.full_name) ⭐\(.stargazers_count) \(.pushed_at[:10]) \(.license.spdx_id // "sin-licencia") — \(.description)"'
   ```
   También sirven las listas «awesome» del tema y, para Android, el catálogo F-Droid (apps abiertas). En `referencias.md` hay apps ya verificadas para las apps de Jeiler.
3. **Filtrar:** licencia clara, actualizada en los últimos 12 meses, con uso real (estrellas como señal, no como prueba).
4. **Para cada una, anotar:**
   - licencia, estrellas, fecha de la última actualización;
   - las funciones principales y las que le faltan;
   - cómo se ve y cómo se usa;
   - **los 10 problemas más comentados**, que son los errores que no hay que repetir:
     ```bash
     gh api -X GET search/issues -f q="repo:DUENO/REPO is:issue sort:comments-desc" -f per_page=10 \
       --jq '.items[] | "\(.comments) comentarios | #\(.number) \(.state) | \(.title)"'
     ```
     (Probado: esta consulta funciona con cualquier repo público. Leer el texto de un problema concreto puede requerir abrirlo en el navegador.)
5. **Tabla final:** qué copiar (solo si la licencia lo permite), qué imitar como idea, qué evitar y por qué.
6. **Especificación corta** para construir la app propia: lista de funciones (primero las esenciales), pantallas, datos que guarda, qué pasa sin internet, los 5 errores de las otras apps que hay que evitar y las fuentes consultadas.
7. **Preguntar al usuario** qué funciones quiere antes de construir. No empezar a programar con la especificación sin su visto bueno.

## Señales de alerta
- Copiar código sin mirar la licencia.
- Elegir una app solo por sus estrellas.
- Reproducir marcas, nombres, íconos o textos de otra app.
- Construir todas las funciones de las apps estudiadas (apps llenas de funciones que nadie pidió).

## Verificación
- [ ] Cada app estudiada tiene licencia y fecha anotadas.
- [ ] Hay una tabla de qué copiar, imitar y evitar.
- [ ] Hay al menos 5 errores de otras apps para no repetir.
- [ ] Nada de código cerrado fue descompilado ni copiado.
- [ ] La especificación la aprobó el usuario.

## Qué se probó (2026-11-04)
Un Claude aparte, con solo esta skill, estudió apps de inventario y préstamo de equipos de laboratorio: la abrió sola, tardó 7 turnos (unos 0,18 USD), comparó 4 apps con su licencia y guardó una `ESPECIFICACION.md`. Las licencias que dio (Snipe-IT, Homebox y Part-DB: AGPL-3.0; InvenTree: MIT) se comprobaron en los repos originales y eran correctas. Distinguió bien qué se puede reutilizar (solo la MIT) y qué solo sirve como idea. Las estrellas de GitHub y las quejas de los usuarios que citó no se comprobaron. No se revisó la calidad de la especificación frente a construir la app.
