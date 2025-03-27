from typing import List

from fastapi import APIRouter, File, Form, UploadFile
from fastapi.responses import FileResponse

from app.agents.toc_agent import generar_tabla_contenido, guardar_tabla_contenido
from app.services.file_loader import save_uploaded_files

router = APIRouter(prefix="/toc", tags=["Tabla de Contenido"])


@router.post("/generar")
def generar_toc_endpoint(
    files: List[UploadFile] = File(...), start_pages: List[int] = Form(...)
):
    # 1. Guardar archivos
    rutas = save_uploaded_files(files)

    # 2. Generar TOC
    toc = generar_tabla_contenido(rutas, start_pages)

    # 3. Guardar TOC como .docx
    output_path = "app/uploads/tabla_contenido_generada.docx"
    guardar_tabla_contenido(toc, output_path)

    return FileResponse(
        path=output_path,
        filename="tabla_contenido.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
