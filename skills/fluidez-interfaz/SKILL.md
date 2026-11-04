---
name: fluidez-interfaz
description: Hace que una interfaz se sienta fluida al moverse entre páginas, pantallas y estados, sin animaciones decorativas. Cubre transiciones de vista (View Transitions), cambios de estado suaves, respuesta inmediata al tocar, esqueletos de carga y respeto por "reducir movimiento". Usar cuando el usuario pida "que se vea más fluido", "transiciones entre páginas", "que no se sienta brusco", "mejorar la interacción" o "cambiar de pantalla suave". No usar para confeti, rebotes ni efectos de adorno.
---

# Fluidez de interacción

La fluidez no es adorno: es que el usuario entienda **de dónde viene y hacia dónde va** cada cambio, y que la app responda al instante.

## Principios
1. **Cada movimiento explica un cambio.** Si no ayuda a entender (entra una pantalla, se abre un panel, un elemento pasa de la lista al detalle), no se anima. Nada de confeti, rebotes largos ni giros.
2. **Respuesta inmediata.** El toque o clic muestra algo en menos de 100 ms (cambio de color, hundimiento del botón). Si la tarea tarda, mostrar un esqueleto de carga, no una pantalla en blanco.
3. **Tiempos cortos.** Cambios pequeños: 150–250 ms. Pantalla completa: 250–400 ms. Nunca más de 400 ms. La salida es más rápida que la entrada.
4. **Solo `transform` y `opacity`.** Animar `width`, `height`, `top` o `left` provoca saltos. Para crecer o moverse, usar `transform: translate/scale`.
5. **El diseño no se mueve solo.** Reservar el espacio de imágenes y anuncios (`aspect-ratio`, alto fijo) para que nada salte al cargar.
6. **Respetar `prefers-reduced-motion`.** Si el usuario pidió menos movimiento, cambiar el movimiento por un fundido simple o ninguno.

## Herramientas, de la más simple a la más compleja
| Necesidad | Qué usar |
|---|---|
| Cambio de página en un sitio normal | CSS `@view-transition { navigation: auto; }` (donde el navegador lo soporte; si no, no pasa nada). |
| Cambio de estado en una sola página | `document.startViewTransition(() => cambiarEstado())`. |
| Un elemento que "viaja" de una vista a otra | `view-transition-name` igual en origen y destino. |
| App en React | Componente `<ViewTransition>`: ver la skill `vercel-react-view-transitions`. |
| Aparecer o desaparecer un panel | Transición CSS de `opacity` y `transform`. |
| Listas que cargan | Esqueletos (`skeleton`) en lugar de ruedas de carga; actualización optimista cuando sea seguro. |
| Efectos de entrada al hacer scroll | Solo si el usuario los pidió; ver GSAP en `ui-ux-pro-max`, con intensidad baja. |

## Móvil
- Áreas táctiles de 44 px mínimo; `touch-action: manipulation` para quitar el retraso del toque.
- Después de navegar, mover el foco al título de la nueva pantalla.
- Probar en un teléfono modesto o simulando CPU lenta: si va fluido ahí, va fluido en todos lados.

## Proceso
1. **Mapear los cambios bruscos:** navegación entre páginas, abrir y cerrar paneles, listas que cargan, formularios que cambian, mensajes que aparecen.
2. **Elegir para cada uno el mecanismo más simple** de la tabla.
3. **Implementar uno por vez**, con el menor código posible.
4. **Comprobar:** recorrer la app con la skill `verificar-app` o `webapp-testing` a 360 px de ancho y con "reducir movimiento" activado; revisar que no haya saltos de diseño y que la respuesta al tocar siga siendo rápida.
5. **Medir** con las herramientas del navegador (Performance, INP) o con la skill `core-web-vitals`.

## Señales de alerta
- Una animación que el usuario tiene que esperar para seguir.
- Movimientos distintos para cosas que son iguales (que todas las pantallas entren igual).
- Efectos que funcionan bien en un computador potente y se traban en un teléfono.
- Animar sin haber probado con "reducir movimiento".

## Verificación
- [ ] Cada transición explica un cambio real.
- [ ] Ninguna dura más de 400 ms.
- [ ] Solo se animan `transform` y `opacity`.
- [ ] Con "reducir movimiento" la app sigue siendo clara.
- [ ] Probado a 360 px de ancho, sin saltos de diseño.
