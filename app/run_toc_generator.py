import os
from pathlib import Path

from app.agents.toc_agent import generar_tabla_contenido, guardar_tabla_contenido

UPLOAD_DIR = Path("app/uploads")
OUTPUT_FILE = UPLOAD_DIR / "tabla_contenido_generada.docx"

# Leer todos los .docx ordenados
docx_files = sorted([str(f) for f in UPLOAD_DIR.glob("*.docx")])

# Páginas ficticias
start_pages = [60 + i * 30 for i in range(len(docx_files))]

# Generar y guardar TOC
toc = generar_tabla_contenido(docx_files, start_pages)
guardar_tabla_contenido(toc, str(OUTPUT_FILE))

print(f"✅ Tabla de contenido generada exitosamente: {OUTPUT_FILE}")
