// MALO a propósito: precarga un archivo que no existe, sin fetch y sin borrar cachés viejas.
const ARCHIVOS = ['./', './index.html', './no-existe.css'];
self.addEventListener('install', (e) => { e.waitUntil(caches.open('v1').then((c) => c.addAll(ARCHIVOS))); });
