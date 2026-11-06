// Mide una PWA en un navegador de verdad (Chromium con Playwright): ¿instala el service worker?, ¿abre SIN INTERNET?,
// ¿el manifest y los íconos cargan y miden lo que dicen?, ¿hay errores de consola?
// Uso:   node medir_pwa.mjs CARPETA_DE_LA_WEB [--playwright-desde CARPETA] [--chromium RUTA]
// Salida: 0 = todo PASA, 1 = algo FALLA, 2 = no se pudo medir (carpeta o Playwright no encontrados).
// Solo escucha en 127.0.0.1 y en un puerto libre; no abre otras redes ni guarda nada. Ver SKILL.md de pwa-completa.
import { createRequire } from 'node:module';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const opc = (n) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : undefined; };
const carpeta = args.find((a, i) => !a.startsWith('--') && !(i > 0 && args[i - 1].startsWith('--')));
if (!carpeta || !fs.existsSync(path.join(carpeta, 'index.html'))) {
  console.error('Uso: node medir_pwa.mjs CARPETA_DE_LA_WEB   (la carpeta debe tener index.html)'); process.exit(2);
}
let pw;
for (const base of [opc('--playwright-desde'), process.env.PLAYWRIGHT_DESDE, process.cwd()].filter(Boolean)) {
  try { pw = createRequire(base.endsWith('/') ? base : base + '/')('playwright'); break; } catch { /* probar el siguiente */ }
}
if (!pw) { try { pw = createRequire(import.meta.url)('playwright'); } catch { /* nada */ } }
if (!pw) { console.error('No encuentro Playwright. Instálalo (npm install playwright) o usa --playwright-desde CARPETA.'); process.exit(2); }

const TIPOS = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json',
  '.webmanifest': 'application/manifest+json', '.png': 'image/png', '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.txt': 'text/plain' };
const raiz = path.resolve(carpeta);
const servidor = http.createServer((req, res) => {
  const ruta = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  let f = path.join(raiz, ruta.endsWith('/') ? ruta + 'index.html' : ruta);
  if (!f.startsWith(raiz + path.sep) && f !== raiz) { res.writeHead(403).end(); return; }  // sin salir de la carpeta
  fs.readFile(f, (e, data) => {
    if (e) { res.writeHead(404).end('no existe'); return; }
    res.writeHead(200, { 'Content-Type': TIPOS[path.extname(f).toLowerCase()] || 'application/octet-stream', 'Cache-Control': 'no-cache' }); res.end(data);
  });
});
await new Promise((ok) => servidor.listen(0, '127.0.0.1', ok));
const url = `http://127.0.0.1:${servidor.address().port}/`;

const res = [];
const chk = (n, ok, d = '') => { res.push(ok); console.log((ok ? 'PASA ' : 'FALLA') + ' | ' + n + (d ? ' | ' + d : '')); };
const info = (n, d) => console.log('INFO  | ' + n + ' | ' + d);

const browser = await pw.chromium.launch({ executablePath: opc('--chromium'), args: ['--no-sandbox', '--disable-dev-shm-usage'] });
const ctx = await browser.newContext({ viewport: { width: 360, height: 740 } });
const page = await ctx.newPage();
const errores = [];
page.on('pageerror', (e) => errores.push('pageerror: ' + e.message.slice(0, 90)));
page.on('console', (m) => { if (m.type() === 'error') errores.push('console.error: ' + m.text().slice(0, 90)); });
page.on('requestfailed', (r) => errores.push('requestfailed: ' + r.url().replace(url, '/')));
page.on('response', (r) => { if (r.status() >= 400) errores.push(`HTTP ${r.status()}: ` + r.url().replace(url, '/')); });
try {
  await page.goto(url, { waitUntil: 'load' });
  const titulo = await page.title();
  // 1. Service worker
  const sw = await page.evaluate(async () => {
    if (!('serviceWorker' in navigator)) return { ok: false, motivo: 'el navegador no soporta service worker' };
    const listo = await Promise.race([navigator.serviceWorker.ready.then(() => true), new Promise((r) => setTimeout(() => r(false), 6000))]);
    const regs = await navigator.serviceWorker.getRegistrations();
    return { ok: listo && regs.length > 0, motivo: regs.length ? 'no llegó a estar activo en 6 s' : 'ninguno registrado' };
  });
  chk('1. el service worker se instala y se activa', sw.ok, sw.ok ? '' : sw.motivo);
  const caches_ = await page.evaluate(async () => { const out = {}; for (const k of await caches.keys()) out[k] = (await (await caches.open(k)).keys()).length; return out; });
  const total = Object.values(caches_).reduce((a, b) => a + b, 0);
  chk('2. la caché tiene archivos guardados', total > 0, JSON.stringify(caches_));
  // 4. Manifest e íconos
  const m = await page.evaluate(async () => {
    const l = document.querySelector('link[rel=manifest]'); if (!l) return { sin_enlace: true };
    try {
      const r = await fetch(l.href); if (!r.ok) return { estado: r.status };
      const man = await r.json(); const iconos = [];
      for (const ic of man.icons || []) {
        const rr = await fetch(new URL(ic.src, l.href)); const item = { src: ic.src, sizes: ic.sizes, estado: rr.status };
        if (rr.ok && /image\/(png|jpeg|webp)/.test(rr.headers.get('content-type') || '')) { const b = await createImageBitmap(await rr.blob()); item.real = b.width + 'x' + b.height; }
        iconos.push(item);
      }
      return { man: { start_url: man.start_url, display: man.display }, iconos };
    } catch (e) { return { error: String(e).slice(0, 60) }; }
  });
  const erroresAlCargar = errores.slice();  // antes de cortar internet (el corte genera sus propios errores)
  // 3. Sin internet
  if (sw.ok) { await page.reload({ waitUntil: 'load' }); await page.waitForTimeout(500); }  // para que el service worker controle la página
  await ctx.setOffline(true);
  let abre = false, detalle = '';
  try {
    await page.reload({ waitUntil: 'load', timeout: 8000 });
    const t2 = await page.title(); const texto = (await page.evaluate(() => document.body.innerText)).trim();
    abre = texto.length > 0 && t2 === titulo; detalle = abre ? '' : `título «${t2}», texto de ${texto.length} caracteres`;
  } catch (e) { detalle = 'sin internet no cargó (' + String(e.message).split('\n')[0].slice(0, 60) + ')'; }
  chk('3. ABRE SIN INTERNET (modo avión) y muestra el mismo contenido', abre, detalle);
  await ctx.setOffline(false);
  if (m.sin_enlace) chk('4. el manifest está enlazado y carga', false, 'no hay <link rel="manifest">');
  else if (m.estado || m.error) chk('4. el manifest está enlazado y carga', false, m.estado ? 'HTTP ' + m.estado : m.error);
  else {
    chk('4. el manifest está enlazado y carga', true, `display=${m.man.display}`);
    const malos = m.iconos.filter((i) => i.estado !== 200 || (i.real && i.sizes && !i.sizes.split(' ').includes(i.real)));
    chk('5. todos los íconos cargan y miden lo que dice el manifest', m.iconos.length > 0 && malos.length === 0,
      malos.map((i) => `${i.src}: HTTP ${i.estado}${i.real ? ', mide ' + i.real + ' y dice ' + i.sizes : ''}`).join('; ') || `${m.iconos.length} ícono(s)`);
  }
  chk('6. sin errores de consola, red ni JavaScript al cargar', erroresAlCargar.length === 0, erroresAlCargar.slice(0, 3).join(' || '));
  info('Alcance', 'Chromium en un perfil limpio; no prueba iPhone, Firefox ni la instalación con el botón del navegador.');
} finally {
  await browser.close(); servidor.close();
}
const fallas = res.filter((x) => !x).length;
console.log(`\n${res.length - fallas} de ${res.length} comprobaciones PASAN.`);
process.exit(fallas ? 1 : 0);
