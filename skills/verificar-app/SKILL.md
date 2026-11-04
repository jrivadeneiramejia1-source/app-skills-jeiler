---
name: verificar-app
description: Verifica que una app web o móvil funciona de verdad antes de darla por terminada. Compila, corre las pruebas, abre la app en un navegador, recorre los flujos principales, revisa errores de consola, accesibilidad, rendimiento y seguridad básica, e intenta romperla con entradas malas. Usar cuando se termina de construir o cambiar una app, antes de subir a main, o cuando el usuario diga "prueba la app", "revisa que no tenga bugs", "verifica que todo funcione", "ataca el código" o "pásale una prueba".
---

# Verificar una app (puerta de calidad)

Objetivo: encontrar los fallos antes que el usuario. Nada se da por bueno sin evidencia: un comando corrido, una captura, un mensaje de error real.

## Reglas
- Solo se prueba lo que es del usuario, en local o en un entorno de pruebas. Nunca atacar sitios de terceros ni datos reales de producción.
- No pedir ni guardar claves. Si la app necesita una, usar una de prueba o decir que falta.
- No cambiar el código mientras se prueba. Primero el informe; los arreglos se hacen después, con permiso, uno por vez.
- Decir siempre qué NO se pudo probar (por ejemplo: teléfono real, sonido, conexiones externas).

## Proceso
1. **Entender la app.** Leer README y archivos de configuración (`package.json`, `wrangler.*`, `firebase.json`). Anotar: tipo (página estática, PWA, Worker, app con Firebase), cómo se instala, cómo se ejecuta, cuáles son los 3 flujos principales.
2. **Compilar y pruebas existentes.** Instalar dependencias, compilar y correr las pruebas. Anotar resultado y cuántas pasaron o fallaron. Si no hay pruebas, decirlo.
3. **Abrirla y usarla.** Levantar la app en local y recorrer los flujos principales con un navegador automático (skills `webapp-testing` o `playwright-cli`). Tomar capturas. Revisar: errores en la consola, peticiones fallidas (4xx/5xx), pantallas en blanco, botones que no responden.
4. **Intentar romperla.** Probar al menos:
   - campos vacíos, textos larguísimos, emojis, caracteres raros, números negativos o con decimales;
   - doble clic rápido, volver atrás, recargar a mitad de un flujo, cerrar y abrir;
   - sin conexión o con conexión lenta;
   - pantalla pequeña (360 px de ancho) y letra grande del sistema;
   - pegar texto con etiquetas HTML o `<script>` en cualquier campo (¿se muestra como texto o se ejecuta?);
   - archivos muy grandes o de tipo equivocado, si la app recibe archivos;
   - **datos guardados dañados** (por ejemplo, escribir texto roto o `[]` en lo que la app guarda en el aparato y recargar);
   - **importar un respaldo dañado** (JSON roto, vacío, de otra forma), si la app lo permite;
   - **doble toque en el botón principal**: ¿guarda dos veces lo mismo?;
   - **recargar sin internet** después de la primera visita (¿abre desde la caché?);
   - **«reducir movimiento»** del sistema: las transiciones deben bajar a casi cero (cuidado: una duración de 0,01 milisegundos es «sin animación», no un fallo).

   Hay una plantilla que hace casi todo esto sola: `plantilla/ataque-web.mjs` (Playwright). Se copia a una carpeta aparte, se escribe un `configuracion.json` con los selectores de la app (el encabezado del archivo explica cada campo) y se corre con `node ataque-web.mjs configuracion.json`. Lo que dé FALLA hay que repetirlo a mano antes de afirmarlo.
5. **Calidad web.** Usar las skills `accessibility`, `performance` y `core-web-vitals` si están disponibles: teclado, contraste, etiquetas, tamaño de los botones táctiles (mínimo 44 px), velocidad de carga y respuesta al tocar.
6. **Seguridad básica.** Buscar claves o tokens escritos en el código (patrones como `api_key`, `secret`, `token`, `AIza`), revisar dependencias con `npm audit` si aplica, revisar las reglas de Firebase con `firebase-security-rules-auditor`, y revisar que el código no se fíe de datos que escribe el usuario. Seguir `security-and-hardening` si está disponible.
7. **Informe.** Tabla simple con tres columnas: **Probado y bien**, **Falló**, **No se pudo probar (y por qué)**. Cada fallo lleva: qué pasó, pasos para repetirlo, gravedad (alta, media, baja) y arreglo sugerido.
8. **Arreglar con permiso.** Un fallo por vez: reproducirlo, arreglarlo, volver a correr la prueba y mostrar que ya pasa. Si hay `systematic-debugging` o `verification-before-completion`, seguirlas.

## Qué se probó (2026-11-04)
Se usó sobre `asesor-prompts` (una app que ya tenía 69 pruebas propias) y encontró **un fallo real** que esas pruebas no cubrían: un doble toque en «Analizar» guarda dos entradas iguales. Además confirmó que la app resiste datos dañados, archivos de respaldo dañados, texto enorme, HTML escrito por el usuario y el modo sin conexión. Con Lighthouse sacó 100 en las cuatro categorías.
- La primera versión de la comprobación de «reducir movimiento» dio un falso fallo (confundió 0,01 ms con una animación); está corregida.
- No se probó en un teléfono real ni con otros navegadores.
- **Activación sola (medida con Sonnet 5.5, 3 frases, 1 a 2 veces cada una):** la skill se abrió sola en 1 de 3 frases («pruébala de arriba abajo»); en «ataca el código» y «rómpela con datos raros» el modelo se puso a trabajar directo sin abrirla. Probé una descripción más larga y no mejoró, así que quedó la original. Para asegurarlo, pedir con su nombre: «usa la skill verificar-app».

## Señales de alerta (parar y decirlo)
- «Debería funcionar» sin haberlo ejecutado.
- Pruebas que pasan pero nunca abrieron la app.
- Un fallo que «solo pasa a veces»: anotarlo, no ignorarlo.
- Una clave real encontrada en el código: avisar de inmediato, sin copiarla en el informe.

## Verificación final
- [ ] Se compiló y se corrieron las pruebas (o se dijo que no hay).
- [ ] Se abrió la app y se recorrieron los flujos principales.
- [ ] Se intentó romperla con entradas malas.
- [ ] El informe dice qué quedó sin probar.
- [ ] Ningún arreglo se hizo sin permiso.
