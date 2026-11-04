// Lighthouse CI (npm run lighthouse): mide velocidad, accesibilidad y buenas prácticas.
// Solo avisa (warn): no frena la publicación. Los informes quedan en .lighthouseci/
// (AJUSTAR) 'url': las páginas a medir, relativas a la carpeta de la app.
// Para otro Chromium: CHROME_PATH=/ruta/al/chromium npm run lighthouse
const avisar = (minimo) => ['warn', { minScore: minimo }];

module.exports = {
  ci: {
    collect: {
      staticDistDir: '.',
      url: ['/index.html'],
      numberOfRuns: 1,
      chromePath: process.env.CHROME_PATH || undefined,
      settings: {
        chromeFlags: '--no-sandbox --disable-dev-shm-usage --headless=new',
        preset: 'desktop'
      }
    },
    assert: {
      assertions: {
        'categories:performance': avisar(0.8),
        'categories:accessibility': avisar(0.95),
        'categories:best-practices': avisar(0.9),
        'categories:seo': 'off'
      }
    },
    upload: { target: 'filesystem', outputDir: '.lighthouseci' }
  }
};
