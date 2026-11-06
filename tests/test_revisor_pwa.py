"""Pruebas de revisar_pwa.py: PWA buena, PWA mala y cambios puntuales hechos a propósito."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SCRIPT = RAIZ / "skills/pwa-completa/scripts/revisar_pwa.py"
EJ = RAIZ / "skills/pwa-completa/ejemplos"


def correr(carpeta, *extra):
    r = subprocess.run([sys.executable, "-I", str(SCRIPT), str(carpeta), *extra], capture_output=True, text=True, timeout=60)
    return r.returncode, r.stdout, r.stderr


def ids(out):
    return {h["id"] for h in json.loads(out)}


class TestRevisorPwa(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.p = self.tmp / "web"
        shutil.copytree(EJ / "pwa-buena", self.p)
        self.html, self.man, self.sw = self.p / "index.html", self.p / "manifest.webmanifest", self.p / "sw.js"

    def cambiar(self, archivo, viejo, nuevo):
        t = archivo.read_text(encoding="utf-8")
        self.assertIn(viejo, t, f"el ejemplo bueno ya no contiene «{viejo}»")
        archivo.write_text(t.replace(viejo, nuevo), encoding="utf-8")

    def manifest(self, **cambios):
        d = json.loads(self.man.read_text(encoding="utf-8"))
        for k, v in cambios.items():
            if v is None:
                d.pop(k, None)
            else:
                d[k] = v
        self.man.write_text(json.dumps(d), encoding="utf-8")

    def esperar(self, regla, grave=None):
        c, out, _ = correr(self.p, "--json")
        self.assertIn(regla, ids(out), f"no saltó {regla}")
        if grave is not None:
            self.assertEqual(c, 1 if grave else 0, regla)

    def test_buena_sale_limpia(self):
        c, out, _ = correr(EJ / "pwa-buena", "--json")
        self.assertEqual((c, json.loads(out)), (0, []))

    def test_mala_detecta_todo(self):
        c, out, _ = correr(EJ / "pwa-mala", "--json")
        self.assertEqual(c, 1)
        esperadas = {"K01", "M02", "M04", "M05", "M06", "M07", "M08", "M09", "P02", "P03", "P04", "P05", "P06", "P07", "P08",
                     "S03", "S04", "S05", "S08", "D01"}
        self.assertTrue(esperadas <= ids(out), f"faltan: {esperadas - ids(out)}")

    def test_no_muestra_valores_secretos(self):
        _, out, _ = correr(EJ / "pwa-mala")
        self.assertNotIn("FAKEFAKE", out)

    def test_html(self):
        self.cambiar(self.html, '<meta name="viewport" content="width=device-width, initial-scale=1>'.replace('1>', '1">'), "")
        self.esperar("P02", True)

    def test_sin_enlace_al_manifest(self):
        self.cambiar(self.html, '<link rel="manifest" href="manifest.webmanifest">', "")
        self.esperar("P01", True)

    def test_manifest_campos(self):
        for campo, regla in (("start_url", "M03"), ("display", "M04"), ("name", None)):
            self.setUp()
            self.manifest(**{campo: None})
            if regla:
                self.esperar(regla, True)
        self.setUp()
        self.manifest(name=None, short_name=None)
        self.esperar("M02", True)

    def test_display_browser_y_prefer_related(self):
        self.manifest(display="browser")
        self.esperar("M04", True)
        self.setUp(); self.manifest(prefer_related_applications=True)
        self.esperar("M08", True)

    def test_iconos(self):
        d = json.loads(self.man.read_text(encoding="utf-8"))
        d["icons"] = [i for i in d["icons"] if "512" not in i["sizes"]]
        self.man.write_text(json.dumps(d), encoding="utf-8")
        self.esperar("M05", True)
        self.setUp()
        (self.p / "iconos/icono-192.png").unlink()
        self.esperar("M05", True)

    def test_icono_de_otro_tamano(self):
        shutil.copy(EJ / "pwa-mala/iconos/icono-192.png", self.p / "iconos/icono-192.png")  # mide 100x100
        self.esperar("M05")

    def test_sin_maskable(self):
        d = json.loads(self.man.read_text(encoding="utf-8"))
        d["icons"] = [i for i in d["icons"] if "purpose" not in i]
        self.man.write_text(json.dumps(d), encoding="utf-8")
        self.esperar("M06", False)

    def test_start_url_absoluta(self):
        self.manifest(start_url="/index.html")
        self.esperar("M09", False)

    def test_json_roto(self):
        self.man.write_text("{ no es json", encoding="utf-8")
        self.esperar("M01", True)

    def test_service_worker(self):
        self.cambiar(self.sw, "'./estilos.css'", "'./estilos-que-no-existe.css'")
        self.esperar("S04", True)
        self.setUp(); self.sw.unlink()
        self.esperar("S02", True)
        self.setUp(); self.cambiar(self.p / "app.js", "navigator.serviceWorker.register('sw.js')", "void 0")
        self.esperar("S01", False)

    def test_service_worker_sin_fetch_ni_limpieza(self):
        self.sw.write_text("const ARCHIVOS = ['./index.html'];\nself.addEventListener('install', (e) => { e.waitUntil(caches.open('v1').then((c) => c.addAll(ARCHIVOS))); });\n", encoding="utf-8")
        c, out, _ = correr(self.p, "--json")
        self.assertTrue({"S03", "S05"} <= ids(out))

    def test_comentario_no_engaña_al_service_worker(self):
        """Un «fetch» o «caches.delete» dentro de un comentario no cuenta."""
        self.sw.write_text("// addEventListener('fetch', ...) y caches.delete(...)\nself.addEventListener('install', (e) => { e.waitUntil(caches.open('v1')); });\n", encoding="utf-8")
        c, out, _ = correr(self.p, "--json")
        self.assertTrue({"S03", "S05"} <= ids(out))

    def test_register_se_resuelve_desde_la_pagina_no_desde_el_js(self):
        """Fallo real encontrado con una app real: js/app.js registraba 'sw.js' y el archivo está junto al index.html."""
        (self.p / "js").mkdir()
        (self.p / "app.js").rename(self.p / "js/app.js")
        self.cambiar(self.html, 'src="app.js"', 'src="js/app.js"')
        c, out, _ = correr(self.p, "--json")
        self.assertNotIn("S02", ids(out))

    def test_ruta_absoluta_bajo_un_prefijo(self):
        """Fallo real encontrado con MDN pwa-examples: register('/mi-app/sw.js') con la web publicada bajo /mi-app/."""
        self.cambiar(self.p / "app.js", "register('sw.js')", f"register('/{self.p.name}/sw.js')")
        c, out, _ = correr(self.p, "--json")
        self.assertNotIn("S02", ids(out))

    def test_enlaces_http_no_son_contenido_mixto(self):
        """Fallo real encontrado con MDN: un <a href="http://..."> es un enlace, no un recurso cargado."""
        self.cambiar(self.html, "<h1>Tareas</h1>", '<h1>Tareas</h1><a href="http://ejemplo.invalid/ayuda">Ayuda</a>')
        c, out, _ = correr(self.p, "--json")
        self.assertNotIn("P07", ids(out))
        self.cambiar(self.html, "<h1>Tareas</h1>", '<h1>Tareas</h1><script src="http://cdn.ejemplo.invalid/x.js"></script>')
        self.esperar("P07", True)

    def test_clave_en_la_web_es_grave_y_en_pruebas_es_media(self):
        (self.p / "config.js").write_text('const k = "AIza' + "B" * 35 + '";\n', encoding="utf-8")
        self.esperar("K01", True)
        (self.p / "config.js").unlink()
        (self.p / "pruebas").mkdir()
        (self.p / "pruebas/clave.mjs").write_text('const k = "AIza' + "B" * 35 + '";\n', encoding="utf-8")
        c, out, _ = correr(self.p, "--json")
        self.assertEqual(c, 0)
        self.assertEqual([h["gravedad"] for h in json.loads(out) if h["id"] == "K01"], ["MEDIA"])

    def test_headers_acepta_no_cache(self):
        (self.p / "_headers").unlink()
        self.esperar("S08", False)

    def test_carpeta_con_www(self):
        envuelta = self.tmp / "proyecto"
        envuelta.mkdir()
        shutil.copytree(self.p, envuelta / "www")
        c, out, _ = correr(envuelta, "--json")
        self.assertEqual((c, json.loads(out)), (0, []))

    def test_errores_de_entrada(self):
        self.assertEqual(correr(self.tmp / "no-existe")[0], 2)
        vacia = self.tmp / "vacia"; vacia.mkdir()
        self.assertEqual(correr(vacia)[0], 2)
        self.assertEqual(subprocess.run([sys.executable, "-I", str(SCRIPT)], capture_output=True).returncode, 2)


if __name__ == "__main__":
    unittest.main()
