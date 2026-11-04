// Plantilla de la skill fluidez-interfaz: mide cuánto duran las animaciones al cambiar de pantalla.
// Uso: node medir-animaciones.mjs URL CARPETA_CON_PLAYWRIGHT "selector1" "selector2" ...
//   URL                 la app, ya sirviéndose (por ejemplo http://localhost:8765/index.html)
//   CARPETA_CON_PLAYWRIGHT  carpeta cuyo node_modules tiene playwright
//   selectorN           botones o pestañas que cambian de pantalla (se hace clic en cada uno)
// Mide en una pantalla de 360 px. Imprime, por cada cambio, cuántas animaciones corren y a los
// cuántos milisegundos termina la última (retraso + duración). La regla de la skill: ≤ 400 ms.
import { createRequire } from 'node:module';
const [url, desde, ...selectores] = process.argv.slice(2);
if (!url || !desde) { console.error('Uso: node medir-animaciones.mjs URL CARPETA_CON_PLAYWRIGHT "selector" ...'); process.exit(2); }
const require = createRequire(desde.endsWith('/') ? desde : desde + '/');
const { chromium } = require('playwright');
const b = await chromium.launch({ executablePath: process.env.CHROMIUM || undefined, args: ['--no-sandbox'] });
const p = await (await b.newContext({ viewport: { width: 360, height: 640 }, hasTouch: true })).newPage();
await p.goto(url); await p.waitForTimeout(800);
const lista = () => p.evaluate(() => document.getAnimations().map((a) => { const t = a.effect.getComputedTiming(); return { n: a.animationName || a.transitionProperty, fin: Math.round(t.duration + t.delay) }; }));
let largas = 0;
for (const s of selectores) {
  await p.click(s); const a = await lista(); const fin = Math.max(0, ...a.map((x) => x.fin)); if (fin > 400) largas++;
  console.log(`${fin > 400 ? 'LARGA' : 'ok   '} | clic en ${s}: ${a.length} animaciones; la última termina a los ${fin} ms (${[...new Set(a.map((x) => x.n + '@' + x.fin))].slice(0, 5).join(', ')})`);
  await p.waitForTimeout(700);
}
const cls = await p.evaluate(() => new Promise((res) => { let t = 0; new PerformanceObserver((l) => { for (const e of l.getEntries()) if (!e.hadRecentInput) t += e.value; }).observe({ type: 'layout-shift', buffered: true }); setTimeout(() => res(t), 500); }));
console.log(`saltos de diseño acumulados (CLS) en esta sesión: ${cls.toFixed(4)} (bueno: menos de 0,1)`);
await b.close();
process.exit(largas ? 1 : 0);
