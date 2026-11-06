"""Pruebas de medir_pwa.mjs (abre Chromium con Playwright). Se saltan solas si no hay Node o Playwright."""
import shutil
import subprocess
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SCRIPT = RAIZ / "skills/pwa-completa/scripts/medir_pwa.mjs"
EJ = RAIZ / "skills/pwa-completa/ejemplos"
NODE = shutil.which("node")


def hay_playwright():
    if not NODE:
        return False
    r = subprocess.run([NODE, "-e", "require('playwright')"], capture_output=True, timeout=60)
    return r.returncode == 0


PLAYWRIGHT = hay_playwright()


def medir(carpeta):
    r = subprocess.run([NODE, str(SCRIPT), str(carpeta)], capture_output=True, text=True, timeout=180)
    return r.returncode, r.stdout, r.stderr


@unittest.skipUnless(PLAYWRIGHT, "Node o Playwright no están instalados (npm install playwright)")
class TestMedirPwa(unittest.TestCase):
    def test_pwa_buena_pasa_las_seis(self):
        c, out, _ = medir(EJ / "pwa-buena")
        self.assertEqual(c, 0, out)
        self.assertIn("6 de 6 comprobaciones PASAN", out)
        self.assertIn("ABRE SIN INTERNET", out)

    def test_pwa_mala_falla_y_no_abre_sin_internet(self):
        c, out, _ = medir(EJ / "pwa-mala")
        self.assertEqual(c, 1)
        fallas = [l for l in out.splitlines() if l.startswith("FALLA")]
        for n in ("1.", "2.", "3.", "5.", "6."):
            self.assertTrue(any(f.split("|")[1].strip().startswith(n) for f in fallas), f"debía fallar la {n}\n{out}")

    def test_mala_coincide_con_el_revisor_estatico(self):
        """Lo que el revisor de texto predice (S04: la precarga falla) se confirma en el navegador (el service worker no se instala)."""
        _, out, _ = medir(EJ / "pwa-mala")
        self.assertIn("ninguno registrado", out)
        self.assertIn('{"v1":0}', out)  # la caché se creó pero quedó vacía

    def test_carpeta_inexistente_da_salida_2(self):
        self.assertEqual(medir(RAIZ / "no-existe")[0], 2)


if __name__ == "__main__":
    unittest.main()
