#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
html2pdf.py — Convierte un HTML (de cualquier skill de agencia) a PDF usando el
navegador que el usuario YA tiene (Chrome / Edge / Brave / Chromium), en modo
headless. Cero dependencias de Python: solo stdlib.

Uso:
    python3 html2pdf.py <archivo.html> [salida.pdf]

Salida:
    - Éxito  → imprime "PDF: <ruta>" y termina con código 0.
    - Sin navegador / falla → imprime "NO_PDF: <motivo>" y termina con código 2.
      (El skill cae al plan B: abrir el HTML y Cmd/Ctrl+P → Guardar como PDF.)

Lo instala el kit en ~/.config/agencia-ia/html2pdf.py y cada skill lo llama
después de generar su HTML. NUNCA descarga ni manda nada a terceros: solo deja
el .pdf junto al .html, en la carpeta del usuario.
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path


def find_browser():
    """Devuelve la ruta a un navegador Chromium-family, o None."""
    # 1) por nombre en el PATH (Linux y instalaciones que lo exponen)
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
                 "brave-browser", "microsoft-edge", "microsoft-edge-stable", "chrome", "msedge"):
        p = shutil.which(name)
        if p:
            return p
    # 2) rutas típicas por sistema operativo
    so = platform.system()
    cands = []
    if so == "Darwin":  # macOS
        cands = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
        ]
    elif so == "Windows":
        bases = [os.environ.get("PROGRAMFILES", ""), os.environ.get("PROGRAMFILES(X86)", ""),
                 os.environ.get("LOCALAPPDATA", "")]
        for b in bases:
            if not b:
                continue
            cands += [
                os.path.join(b, "Google", "Chrome", "Application", "chrome.exe"),
                os.path.join(b, "Microsoft", "Edge", "Application", "msedge.exe"),
                os.path.join(b, "BraveSoftware", "Brave-Browser", "Application", "brave.exe"),
                os.path.join(b, "Chromium", "Application", "chrome.exe"),
            ]
    else:  # Linux y otros
        cands = [
            "/usr/bin/google-chrome", "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium", "/usr/bin/chromium-browser",
            "/usr/bin/brave-browser", "/usr/bin/microsoft-edge",
            "/snap/bin/chromium",
        ]
    for c in cands:
        if c and os.path.exists(c):
            return c
    return None


def to_pdf(browser, url, pdf_path):
    """Intenta render headless. Prueba flags nuevos y, si falla, los clásicos."""
    variantes = [
        [browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         "--print-to-pdf=" + pdf_path, url],
        [browser, "--headless", "--disable-gpu",
         "--print-to-pdf=" + pdf_path, url],
    ]
    for cmd in variantes:
        try:
            subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        except Exception:
            continue
        if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
            return True
    return False


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 html2pdf.py <archivo.html> [salida.pdf]")
        sys.exit(1)
    html = Path(sys.argv[1]).expanduser().resolve()
    if not html.is_file():
        print("NO_PDF: no encontré el HTML: {}".format(html))
        sys.exit(2)
    pdf = Path(sys.argv[2]).expanduser().resolve() if len(sys.argv) > 2 else html.with_suffix(".pdf")

    browser = find_browser()
    if not browser:
        print("NO_PDF: no encontré Chrome/Edge/Brave/Chromium. Abre el HTML y haz "
              "Cmd/Ctrl+P → Guardar como PDF.")
        sys.exit(2)

    if to_pdf(browser, html.as_uri(), str(pdf)):
        print("PDF: {}".format(pdf))
        sys.exit(0)

    print("NO_PDF: el navegador no pudo generar el PDF. Abre el HTML y haz "
          "Cmd/Ctrl+P → Guardar como PDF.")
    sys.exit(2)


if __name__ == "__main__":
    main()
