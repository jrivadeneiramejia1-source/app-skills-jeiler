// Plantilla de la skill verificar-app: intenta romper una app web con Playwright.
// Uso:  node ataque-web.mjs configuracion.json
// La app debe estar sirviéndose (por ejemplo: python3 -m http.server 8765 dentro de su carpeta).
// Cada comprobación imprime PASA, FALLA o INFO. Sale con código 1 si algo FALLA.
//
// configuracion.json (todo es opcional salvo "url" y "playwrightDesde"):
// {
//   "url": "http://localhost:8765/index.html",
//   "playwrightDesde": "/ruta/del/proyecto/",         // carpeta cuyo node_modules tiene playwright
//   "chromium": "/opt/pw-browsers/chromium",          // ruta de Chromium, si no es la de Playwright
//   "campoTexto": "#borrador",                        // campo donde el usuario escribe
//   "botonEnviar": "#btnAnalizar",                    // botón principal
//   "resultado": "#resultado",                        // elemento que se ve cuando hay resultado
//   "pestanas": ["[data-vista=\"historial\"]", "[data-vista=\"ajustes\"]"],  // botones de navegación
//   "historial": { "pestana": "[data-vista=\"historial\"]", "items": "#lista > *" },
//   "archivoImportar": "#archivo"                     // <input type=file> de importar respaldo
// }
import { createRequire } from 'node:module';
import fs from 'node:fs';
const cfg = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const require = createRequire(cfg.playwrightDesde.endsWith('/') ? cfg.playwrightDesde : cfg.playwrightDesde + '/');
const { chromium } = require('playwright');
const res = [];
const chk = (n, ok, d = '') => { res.push({ n, ok, d }); console.log((ok ? 'PASA ' : 'FALLA') + ' | ' + n + (d ? ' | ' + d : '')); };
const info = (n, d) => { res.push({ n, ok: null, d }); console.log('INFO  | ' + n + ' | ' + d); };
const browser = await chromium.launch({ executablePath: cfg.chromium, args: ['--no-sandbox', '--disable-dev-shm-usage'] });
async function nueva(opts = {}) {
  const ctx = await browser.newContext({ viewport: { width: 1000, height: 800 }, ...opts });
  const page = await ctx.newPage(); const errores = [];
  page.on('pageerror', (e) => errores.push('pageerror: ' + e.message));
  page.on('console', (m) => { if (m.type() === 'error') errores.push('console.error: ' + m.text()); });
  page.on('requestfailed', (r) => errores.push('requestfailed: ' + r.url()));
  return { ctx, page, errores };
}
const enviar = async (page, texto) => { await page.fill(cfg.campoTexto, texto); await page.click(cfg.botonEnviar); await page.waitForTimeout(400); };
const hayResultado = (page) => (cfg.resultado ? page.locator(cfg.resultado).isVisible() : Promise.resolve(true));

// 1. Carga inicial
{ const { ctx, page, errores } = await nueva(); await page.goto(cfg.url); await page.waitForTimeout(800);
  chk('1. carga inicial sin errores de consola, red ni JavaScript', errores.length === 0, errores.join(' || ').slice(0, 200));
  const sw = await page.evaluate(async () => { try { const r = await navigator.serviceWorker.ready; return !!r.active; } catch { return false; } });
  info('1b. service worker activo', String(sw)); await ctx.close(); }
if (cfg.campoTexto && cfg.botonEnviar) {
  // 2. Vacío
  { const { ctx, page, errores } = await nueva(); await page.goto(cfg.url); await page.waitForTimeout(400);
    await page.click(cfg.botonEnviar); await page.waitForTimeout(400);
    chk('2. enviar vacío no rompe ni inventa un resultado', errores.length === 0 && !(await hayResultado(page)), `errores=${errores.length}`); await ctx.close(); }
  // 3. Normal
  { const { ctx, page, errores } = await nueva(); await page.goto(cfg.url); await page.waitForTimeout(400);
    await enviar(page, 'texto normal de prueba para la app'); chk('3. texto normal: hay resultado y no hay errores', (await hayResultado(page)) && errores.length === 0, errores.join(' || ').slice(0, 150)); await ctx.close(); }
  // 4. Caracteres raros
  { const { ctx, page, errores } = await nueva(); await page.goto(cfg.url); await page.waitForTimeout(400);
    for (const [n, t] of [['emojis', '🔥💻😭 '.repeat(40)], ['cero-ancho y derecha a izquierda', 'hola​‍mundo ‮abc‬ مرحبا'], ['control', 'a\u0001b\u0007c\u001bd'], ['solo espacios y saltos', '   \n\n\t \n'], ['palabra de 5000 letras', 'a'.repeat(5000)], ['plantillas', '{{7*7}} ${7*7} <%= 7*7 %>']]) {
      errores.length = 0; try { await enviar(page, t); } catch (e) { errores.push('excepción: ' + e.message); }
      chk('4. «' + n + '» no rompe', errores.length === 0, errores.join(' || ').slice(0, 150)); } await ctx.close(); }
  // 5. XSS
  { const { ctx, page } = await nueva(); await page.goto(cfg.url); await page.waitForTimeout(400);
    await enviar(page, '<img src=x onerror="window.__xss=1"> <script>window.__xss=2</script> "><svg onload="window.__xss=3">');
    if (cfg.historial) { await page.click(cfg.historial.pestana); await page.waitForTimeout(300); }
    const r = await page.evaluate(() => ({ x: window.__xss, n: document.querySelectorAll('img[src="x"], svg[onload]').length }));
    chk('5. HTML y scripts escritos por el usuario NO se ejecutan', r.x === undefined && r.n === 0, `__xss=${r.x} inyectados=${r.n}`); await ctx.close(); }
  // 6. Texto enorme
  { const { ctx, page, errores } = await nueva(); await page.goto(cfg.url); await page.waitForTimeout(400);
    const t0 = Date.now(); let error = '';
    try { await page.fill(cfg.campoTexto, 'Necesito ayuda con una automatización que lea correos. '.repeat(6000), { timeout: 20000 }); await page.click(cfg.botonEnviar); await page.waitForTimeout(500); } catch (e) { error = e.message.slice(0, 80); }
    const vivo = await page.evaluate(() => 1 + 1).catch(() => null);
    chk('6. con ~300 mil caracteres la página sigue respondiendo (< 8 s)', Date.now() - t0 < 8000 && vivo === 2 && !error, `${Date.now() - t0} ms ${error}`); await ctx.close(); }
  // 7. Doble toque
  if (cfg.historial) { const { ctx, page } = await nueva(); await page.goto(cfg.url); await page.waitForTimeout(400);
    await page.fill(cfg.campoTexto, 'texto para el doble toque'); await page.dblclick(cfg.botonEnviar); await page.waitForTimeout(600);
    await page.click(cfg.historial.pestana); await page.waitForTimeout(300);
    const n = await page.locator(cfg.historial.items).count();
    chk('7. un doble toque en el botón principal guarda UNA sola entrada', n === 1, `entradas=${n}`); await ctx.close(); }
}
// 8. Atrás y recargar
if (cfg.pestanas && cfg.pestanas.length >= 2) { const { ctx, page, errores } = await nueva(); await page.goto(cfg.url); await page.waitForTimeout(400);
  await page.click(cfg.pestanas[0]); await page.waitForTimeout(200); const h0 = await page.evaluate(() => location.hash);
  await page.click(cfg.pestanas[1]); await page.waitForTimeout(200); await page.goBack(); await page.waitForTimeout(300);
  const h1 = await page.evaluate(() => location.hash);
  chk('8. el botón Atrás vuelve a la pantalla anterior', h1 === h0, `antes=${h0} después=${h1}`);
  await page.reload(); await page.waitForTimeout(500); chk('8b. recargar no genera errores', errores.length === 0, errores.join(' || ').slice(0, 150)); await ctx.close(); }
// 9. Datos guardados dañados
{ const { ctx, page, errores } = await nueva(); await page.goto(cfg.url); await page.waitForTimeout(400);
  if (cfg.campoTexto && cfg.botonEnviar) await enviar(page, 'dato para guardar');
  const claves = await page.evaluate(() => Object.keys(localStorage)); info('9. claves guardadas en el aparato', claves.join(', ') || '(ninguna)');
  for (const [n, v] of [['texto que no es JSON', '{{{no es json'], ['forma equivocada ([])', '[]'], ['nulo', 'null']]) {
    await page.evaluate((valor) => { for (const k of Object.keys(localStorage)) localStorage.setItem(k, valor); }, v); errores.length = 0;
    await page.reload(); await page.waitForTimeout(600); chk('9. datos guardados dañados («' + n + '»): la app abre sin errores', errores.length === 0, errores.join(' || ').slice(0, 160)); }
  await ctx.close(); }
// 10. Importar un archivo dañado
if (cfg.archivoImportar) { const { ctx, page, errores } = await nueva(); await page.goto(cfg.url); await page.waitForTimeout(400);
  if (cfg.pestanas) { await page.click(cfg.pestanas[cfg.pestanas.length - 1]); await page.waitForTimeout(300); }
  for (const [n, c] of [['JSON roto', '{no es json'], ['JSON de otra forma', '{"hola":1}'], ['vacío', ''], ['un arreglo', '[1,2,3]']]) {
    errores.length = 0; await page.setInputFiles(cfg.archivoImportar, { name: 'respaldo.json', mimeType: 'application/json', buffer: Buffer.from(c) }); await page.waitForTimeout(500);
    chk('10. importar un archivo «' + n + '» no rompe', errores.length === 0, errores.join(' || ').slice(0, 150)); } await ctx.close(); }
// 11. Pantalla de 360 px
{ const { ctx, page } = await nueva({ viewport: { width: 360, height: 640 }, hasTouch: true, isMobile: true }); await page.goto(cfg.url); await page.waitForTimeout(500);
  const vistas = [null, ...(cfg.pestanas || [])];
  for (const [i, sel] of vistas.entries()) { if (sel) { await page.click(sel); await page.waitForTimeout(250); }
    const r = await page.evaluate(() => ({ sw: document.documentElement.scrollWidth, iw: window.innerWidth }));
    chk(`11. 360 px, pantalla ${i + 1}: sin desplazamiento horizontal`, r.sw <= r.iw + 1, `contenido=${r.sw} pantalla=${r.iw}`);
    const chicos = await page.evaluate(() => [...document.querySelectorAll('button, a, input, select, textarea, summary')].filter((e) => e.offsetParent !== null).map((e) => { const b = e.getBoundingClientRect(); return { t: (e.innerText || e.id || e.tagName).trim().replace(/\s+/g, ' ').slice(0, 22), w: Math.round(b.width), h: Math.round(b.height) }; }).filter((x) => x.w < 44 || x.h < 44));
    if (chicos.length) info(`11b. 360 px, pantalla ${i + 1}: táctiles menores a 44 px`, chicos.map((c) => `${c.t}(${c.w}x${c.h})`).join(', ').slice(0, 240)); }
  await ctx.close(); }
// 12. Sin conexión
{ const { ctx, page } = await nueva(); await page.goto(cfg.url); await page.waitForTimeout(1500);
  await page.evaluate(async () => { try { await navigator.serviceWorker.ready; } catch {} }); await page.reload(); await page.waitForTimeout(800);
  await ctx.setOffline(true); let abre = false;
  try { await page.reload({ timeout: 8000 }); await page.waitForTimeout(500); abre = (await page.title()).length > 0; } catch { abre = false; }
  info('12. sin conexión, ¿abre desde la caché?', abre ? 'sí' : 'no (si la app debía funcionar sin internet, es un fallo)'); await ctx.close(); }
// 13. Reducir movimiento
{ const medir = async (opts) => { const { ctx, page } = await nueva(opts); await page.goto(cfg.url); await page.waitForTimeout(600);
    const m = await page.evaluate(() => { let max = 0; for (const e of document.querySelectorAll('*')) { const s = getComputedStyle(e); max = Math.max(max, ...s.transitionDuration.split(',').map(parseFloat), ...s.animationDuration.split(',').map(parseFloat)); } return max; }); await ctx.close(); return m; };
  const normal = await medir({}), reducido = await medir({ reducedMotion: 'reduce' });
  info('13. duración máxima de transiciones', `normal=${normal} s, con «reducir movimiento»=${reducido} s`);
  chk('13b. «reducir movimiento» baja las transiciones a casi cero (≤ 0,05 s)', reducido <= 0.05, `${reducido} s`);
  chk('13c. ninguna transición normal pasa de 0,4 s', normal <= 0.4, `${normal} s`); }
// 14. Teclado
{ const { ctx, page } = await nueva(); await page.goto(cfg.url); await page.waitForTimeout(500); const sin = [];
  for (let i = 0; i < 14; i++) { await page.keyboard.press('Tab');
    const f = await page.evaluate(() => { const e = document.activeElement; if (!e || e === document.body) return null; const s = getComputedStyle(e); return { t: (e.innerText || e.id || e.tagName).trim().slice(0, 22), v: (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0) || s.boxShadow !== 'none' }; });
    if (f && !f.v) sin.push(f.t); }
  chk('14. con Tab, cada elemento muestra el foco', sin.length === 0, 'sin foco: ' + sin.join(', ')); await ctx.close(); }
await browser.close();
const f = res.filter((r) => r.ok === false);
console.log(`\nRESUMEN: ${res.filter((r) => r.ok === true).length} pasan, ${f.length} fallan, ${res.filter((r) => r.ok === null).length} informativos`);
process.exit(f.length ? 1 : 0);
