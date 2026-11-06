#!/usr/bin/env python3
"""Revisa una PWA (web instalable) que está en una carpeta, sin abrir un navegador.

Uso:   python -I revisar_pwa.py CARPETA_DE_LA_WEB [--json]
Salida: 0 = sin hallazgos graves, 1 = hay hallazgos ALTA, 2 = no se pudo leer.

Solo lee archivos de texto y los tamaños de los íconos PNG: no abre redes, no ejecuta el JavaScript
de la web y NUNCA imprime el valor de una clave. Busca patrones; que salga limpio NO prueba que la
PWA funcione sin internet (eso se prueba con un navegador: ver SKILL.md).
"""
import json
import os
import re
import struct
import sys
from pathlib import Path
from urllib.parse import urlparse

MAX_ARCHIVO = 2_000_000
DISPLAY_OK = {"standalone", "fullscreen", "minimal-ui", "window-controls-overlay"}
CLAVES = [
    ("token de bot de Telegram", re.compile(r"(?<!\d)\d{8,10}:[A-Za-z0-9_-]{35}(?![A-Za-z0-9_-])")),
    ("clave tipo sk-...", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}")),
    ("clave de Google (AIza...)", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("token de GitHub", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}")),
    ("llave privada", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
]
MARCADOR = re.compile(r"(?i)(your[_ -]|insert|replace|change[_-]?me|xxx|<[^<>]{2,}>|example|placeholder)")
SALTAR = {"node_modules", ".git", "dist-old", "__pycache__"}
PRUEBAS = {"test", "tests", "pruebas", "__tests__", "spec", "e2e", "fixtures"}


def leer(p):
    try:
        return p.read_text(encoding="utf-8", errors="replace") if p.stat().st_size <= MAX_ARCHIVO else ""
    except OSError:
        return ""


def sin_comentarios_js(t):
    t = re.sub(r"/\*.*?\*/", "", t, flags=re.S)
    return re.sub(r"(?<![:\"'\\])//[^\n]*", "", t)


def tamano_png(p):
    try:
        with open(p, "rb") as f:
            cab = f.read(24)
        if cab[:8] == b"\x89PNG\r\n\x1a\n" and cab[12:16] == b"IHDR":
            return struct.unpack(">II", cab[16:24])
    except OSError:
        pass
    return None


def es_externa(ruta):
    return bool(re.match(r"^(https?:)?//|^data:|^blob:|^mailto:|^tel:|^#", ruta.strip(), re.I))


def a_disco(base_dir, ruta, raiz):
    """Convierte una ruta de la web en un archivo del disco (sin ?query ni #ancla). None si no aplica."""
    ruta = ruta.split("#")[0].split("?")[0].strip()
    if not ruta or es_externa(ruta):
        return None
    if not ruta.startswith("/"):
        return base_dir / ruta
    # Ruta absoluta: la web puede estar publicada bajo un prefijo (/mi-app/sw.js). Se prueba quitando carpetas del principio.
    partes = [x for x in ruta.split("/") if x]
    for i, seg in enumerate(partes):  # /mi-app/lo-que-sea: «mi-app» es la propia carpeta de la web
        if seg == raiz.name and raiz.joinpath(*partes[i + 1:]).exists():
            return raiz.joinpath(*partes[i + 1:])
    for i in range(len(partes)):
        cand = raiz.joinpath(*partes[i:])
        if cand.exists():
            return cand
    return raiz.joinpath(*partes) if partes else raiz


def buscar_raiz(arg):
    base = Path(arg)
    if not base.is_dir():
        raise ValueError(f"no encuentro la carpeta: {arg}")
    for cand in [base] + [base / n for n in ("www", "public", "dist", "docs", "build", "src")]:
        if (cand / "index.html").is_file():
            return cand
    for dp, dirs, files in os.walk(base):
        dirs[:] = [d for d in dirs if d not in SALTAR]
        if "index.html" in files:
            return Path(dp)
    raise ValueError("no encontré un index.html en la carpeta")


def revisar(arg):
    raiz = buscar_raiz(arg)
    rel = lambda p: str(p.relative_to(raiz)) if raiz in p.parents or p == raiz else p.name  # noqa: E731
    h = []

    def add(id_, grav, donde, texto):
        h.append({"id": id_, "gravedad": grav, "donde": donde, "texto": texto})

    html_p = raiz / "index.html"
    html = leer(html_p)
    if not html.strip():
        raise ValueError("el index.html está vacío")
    low = html.lower()

    # ---- HTML
    if not re.search(r"<meta[^>]+name=[\"']viewport[\"']", low):
        add("P02", "ALTA", "index.html", "Falta <meta name=\"viewport\">: en el teléfono la página se ve diminuta.")
    if not re.search(r"<html[^>]+\blang=", low):
        add("P03", "MEDIA", "index.html", "Falta lang en <html>: los lectores de pantalla pronuncian mal el texto.")
    if not re.search(r"<title>\s*\S", low):
        add("P05", "MEDIA", "index.html", "Falta <title>: es el nombre que sale en la pestaña y al instalar.")
    if not re.search(r"<meta[^>]+name=[\"']theme-color[\"']", low):
        add("P04", "BAJA", "index.html", "Falta <meta name=\"theme-color\">: la barra del navegador no toma el color de la app.")
    sin_alt = [m for m in re.findall(r"<img\b[^>]*>", html, re.I) if not re.search(r"\balt\s*=", m, re.I)]
    if sin_alt:
        add("P06", "MEDIA", "index.html", f"{len(sin_alt)} imagen(es) sin atributo alt (alt=\"\" si es decorativa).")

    # ---- Manifest
    m_link = re.search(r"<link[^>]+rel=[\"']manifest[\"'][^>]*>", html, re.I)
    manifest_p = None
    if not m_link:
        add("P01", "ALTA", "index.html", "No hay <link rel=\"manifest\">: el navegador no ofrece instalar la app.")
        for n in ("manifest.webmanifest", "manifest.json"):
            if (raiz / n).is_file():
                manifest_p = raiz / n
                add("P01", "BAJA", n, "El archivo del manifest existe pero no está enlazado desde index.html.")
                break
    else:
        href = re.search(r"href=[\"']([^\"']+)", m_link.group(0))
        if href:
            manifest_p = a_disco(raiz, href.group(1), raiz)
    man = None
    if manifest_p is not None:
        if not manifest_p.is_file():
            add("M01", "ALTA", rel(manifest_p) if manifest_p.exists() else str(manifest_p.name), "El manifest está enlazado pero el archivo no existe.")
        else:
            try:
                man = json.loads(leer(manifest_p))
            except json.JSONDecodeError:
                add("M01", "ALTA", rel(manifest_p), "El manifest no es un JSON válido (¿coma de más?).")
    if isinstance(man, dict):
        donde = rel(manifest_p)
        if not man.get("name") and not man.get("short_name"):
            add("M02", "ALTA", donde, "Falta name o short_name (Chrome pide al menos uno).")
        elif not man.get("short_name"):
            add("M02", "BAJA", donde, "Falta short_name: es el texto corto bajo el ícono.")
        if not man.get("start_url"):
            add("M03", "ALTA", donde, "Falta start_url (Chrome lo pide para instalar).")
        if man.get("display") not in DISPLAY_OK:
            add("M04", "ALTA", donde, "display debe ser standalone, fullscreen, minimal-ui o window-controls-overlay (Chrome lo pide para instalar).")
        if man.get("prefer_related_applications") is True:
            add("M08", "ALTA", donde, "prefer_related_applications está en true: Chrome no ofrece instalar la PWA.")
        for campo in ("theme_color", "background_color"):
            if not man.get(campo):
                add("M07", "BAJA", donde, f"Falta {campo}.")
        for campo in ("start_url", "scope"):
            v = man.get(campo)
            if isinstance(v, str) and v.startswith("/") and not v.startswith("//"):
                add("M09", "MEDIA", donde, f"{campo} empieza con «/»: en una subcarpeta (GitHub Pages: usuario.github.io/mi-app/) apunta al sitio equivocado. Usa «./».")
        su = man.get("start_url")
        if isinstance(su, str) and not es_externa(su):
            p = a_disco(manifest_p.parent, su, raiz)
            if p is not None and not su.startswith("/") and su.split("?")[0].split("#")[0] not in ("", ".", "./") and not p.exists():
                add("M10", "MEDIA", donde, "start_url apunta a un archivo que no existe en la carpeta.")
        iconos = man.get("icons") if isinstance(man.get("icons"), list) else []
        tamanos, maskable = set(), False
        for ic in iconos:
            if not isinstance(ic, dict):
                continue
            src = ic.get("src", "")
            declarados = str(ic.get("sizes", "")).split()
            for s in declarados:
                tamanos.add(s.lower())
            if "maskable" in str(ic.get("purpose", "")):
                maskable = True
            p = a_disco(manifest_p.parent, src, raiz) if src else None
            if p is not None:
                if not p.is_file():
                    add("M05", "ALTA", donde, f"El ícono «{os.path.basename(src)}» está en el manifest pero el archivo no existe.")
                elif p.suffix.lower() == ".png" and declarados:
                    real = tamano_png(p)
                    if real and f"{real[0]}x{real[1]}" not in [s.lower() for s in declarados]:
                        add("M05", "MEDIA", donde, f"El ícono «{os.path.basename(src)}» mide {real[0]}x{real[1]} pero el manifest dice {' '.join(declarados)}.")
        if not ({"192x192", "512x512"} <= tamanos or "any" in tamanos):
            add("M05", "ALTA", donde, "Chrome pide un ícono de 192x192 y otro de 512x512 en el manifest.")
        if iconos and not maskable:
            add("M06", "MEDIA", donde, "Ningún ícono tiene purpose \"maskable\": en Android el ícono puede verse recortado o con fondo blanco.")

    # ---- Service worker
    archivos_js = [p for p in raiz.rglob("*") if p.suffix in (".js", ".mjs", ".html") and p.is_file()
                   and not (SALTAR & set(p.relative_to(raiz).parts))]
    textos = {p: leer(p) for p in archivos_js}
    sw_ref = None
    for p, t in textos.items():
        m = re.search(r"serviceWorker\s*\.\s*register\(\s*[\"'`]([^\"'`]+)", sin_comentarios_js(t) if p.suffix != ".html" else t)
        if m:
            sw_ref = (p, m.group(1))
            break
    if not sw_ref:
        add("S01", "MEDIA", "(web)", "No encontré navigator.serviceWorker.register(): sin service worker la app no abre sin internet.")
    else:
        # register() resuelve la ruta respecto de la página, no del archivo .js que lo llama
        sw_p = a_disco(sw_ref[0].parent if sw_ref[0].suffix == ".html" else raiz, sw_ref[1], raiz)
        if sw_p is None or not sw_p.is_file():
            add("S02", "ALTA", rel(sw_ref[0]), f"Se registra «{os.path.basename(sw_ref[1].split('?')[0])}» pero ese archivo no existe.")
        else:
            sw = sin_comentarios_js(leer(sw_p))
            if not re.search(r"addEventListener\(\s*[\"']fetch[\"']|\bonfetch\b", sw):
                add("S03", "MEDIA", rel(sw_p), "El service worker no responde al evento fetch: no sirve nada desde la caché, no abre sin internet.")
            if "caches.delete" not in sw and re.search(r"caches\.open", sw):
                add("S05", "MEDIA", rel(sw_p), "No borra cachés viejas (caches.delete): al cambiar la versión se acumulan y puede seguir mostrando archivos viejos.")
            # S04: archivos de la lista de precarga que no existen (addAll falla y el service worker no se instala)
            lista = None
            m = re.search(r"addAll\(\s*(\[[^\]]*\])", sw, re.S)
            if m:
                lista = m.group(1)
            else:
                m = re.search(r"addAll\(\s*([A-Za-z_$][\w$]*)\s*\)", sw)
                if m:
                    v = re.search(r"(?:const|let|var)\s+" + re.escape(m.group(1)) + r"\s*=\s*(\[[^\]]*\])", sw, re.S)
                    lista = v.group(1) if v else None
            if lista:
                faltan = []
                for ruta in re.findall(r"[\"'`]([^\"'`]+)[\"'`]", lista):
                    p = a_disco(sw_p.parent, ruta, raiz)
                    if p is None:
                        continue
                    if p.is_dir() or ruta.split("?")[0].endswith("/"):
                        if not (p / "index.html").is_file():
                            faltan.append(ruta)
                    elif not p.exists():
                        faltan.append(ruta)
                if faltan:
                    add("S04", "ALTA", rel(sw_p), f"La lista de precarga incluye {len(faltan)} archivo(s) que no existen ({', '.join(os.path.basename(x.rstrip('/')) or x for x in faltan[:4])}): cache.addAll falla y el service worker no se instala.")
            # S08: que el navegador no guarde sw.js por días
            hd = leer(raiz / "_headers")
            if not re.search(r"(?is)sw\.js[^\n]*\n(?:[ \t]+[^\n]*\n)*?[ \t]+cache-control:[^\n]*(no-cache|max-age=0|no-store)", hd + "\n") \
                    and not re.search(r"(?is)/\*[^\n]*\n(?:[ \t]+[^\n]*\n)*?[ \t]+cache-control:[^\n]*(no-cache|max-age=0)", hd + "\n"):
                add("S08", "BAJA", "(servidor)", "No veo un _headers que evite guardar sw.js en caché. En Cloudflare Pages se pone en un archivo _headers; sin eso las actualizaciones pueden tardar días en llegar.")

    # ---- Rutas, contenido mixto, datos y claves
    codigo = {p: t for p, t in textos.items()}
    for p, t in list(codigo.items()):
        # P07 contenido mixto: solo recursos que se cargan (no enlaces <a href>, ni xmlns)
        for m in re.finditer(r"<(script|link|img|iframe|source|video|audio|embed)\b[^>]*?\b(?:src|href)\s*=\s*[\"'](http://(?!localhost|127\.0\.0\.1)[^\"']+)", t, re.I):
            tag = m.group(1).lower()
            grave = tag == "script" or (tag == "link" and re.search(r"rel=[\"'](stylesheet|manifest|preload)", m.group(0), re.I))
            add("P07", "ALTA" if grave else "MEDIA", rel(p), "Carga un recurso por http:// (sin cifrar): el navegador lo bloquea en una página https.")
            break
        else:
            if re.search(r"\bfetch\(\s*[\"'`]http://(?!localhost|127\.0\.0\.1)", t):
                add("P07", "MEDIA", rel(p), "Pide datos por http:// (sin cifrar): el navegador lo bloquea en una página https.")
    # P08 rutas absolutas
    abs_hits = re.findall(r"""(?:src|href)\s*=\s*["'](/(?!/)[^"']*)""", html, re.I)
    if abs_hits:
        add("P08", "MEDIA", "index.html", f"{len(abs_hits)} ruta(s) empiezan con «/» (por ejemplo {abs_hits[0][:30]}): se rompen si la app vive en una subcarpeta (GitHub Pages). Usa rutas relativas.")
    # D01 datos sin exportar
    todo_js = "\n".join(sin_comentarios_js(t) if p.suffix != ".html" else t for p, t in codigo.items())
    if re.search(r"localStorage|indexedDB", todo_js) and not re.search(r"new\s+Blob\(|download\s*=|createObjectURL|showSaveFilePicker", todo_js):
        add("D01", "BAJA", "(web)", "Guarda datos en el dispositivo pero no veo cómo exportarlos. El navegador puede borrarlos: ofrece exportar e importar un archivo.")
    # K01 claves (en carpetas de pruebas es MEDIA: normalmente son valores inventados para probar un detector)
    for p, t in codigo.items():
        en_pruebas = bool(PRUEBAS & {x.lower() for x in p.relative_to(raiz).parts[:-1]}) or bool(re.search(r"\.(test|spec)\.", p.name))
        vistos = set()
        for etiqueta, rx in CLAVES:
            m = rx.search(t)
            if m and not MARCADOR.search(m.group(0)) and etiqueta not in vistos:
                vistos.add(etiqueta)
                if en_pruebas:
                    add("K01", "MEDIA", rel(p), f"Parece haber un {etiqueta} en un archivo de pruebas. Confirma que es inventado; si es real, cámbialo en el servicio.")
                else:
                    add("K01", "ALTA", rel(p), f"Parece haber un {etiqueta} escrito en el archivo. Cualquiera que abra la web lo puede leer: quítalo y cámbialo en el servicio.")
    return h


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    if len(args) != 1:
        print("Uso: python -I revisar_pwa.py CARPETA_DE_LA_WEB [--json]", file=sys.stderr)
        return 2
    try:
        hallazgos = revisar(args[0])
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    orden = {"ALTA": 0, "MEDIA": 1, "BAJA": 2}
    hallazgos.sort(key=lambda x: (orden[x["gravedad"]], x["id"], x["donde"]))
    if "--json" in argv:
        print(json.dumps(hallazgos, ensure_ascii=False, indent=2))
    else:
        if not hallazgos:
            print("Sin hallazgos. (No prueba que abra sin internet: pruébalo en el navegador en modo avión.)")
        for x in hallazgos:
            print(f"[{x['gravedad']}] {x['id']} · {x['donde']}: {x['texto']}")
        print(f"\n{len(hallazgos)} hallazgo(s), {sum(1 for x in hallazgos if x['gravedad'] == 'ALTA')} grave(s).")
    return 1 if any(x["gravedad"] == "ALTA" for x in hallazgos) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
