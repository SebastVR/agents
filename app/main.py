from crewai import Crew, Task
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer

from app.agents.toc_agent import (
    crear_agente_toc,
    crear_doc_tabla_contenido,
    extraer_headings_desde_docx,
)

# from app.agents.toc_agent import crear_agente_toc

# from app.agents.toc_generator import generate_toc_and_merge
# from app.agents.toc_generator import combinar_documentos
# from app.agents.toc_generator import generar_tabla_contenido

# from app.routers import toc_router

api = FastAPI(title="Document Storage API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# api.include_router(toc_router.router)


# Punto de entrada opcional para testing
@api.get("/")
def root():
    return {"message": "Bienvenido al agente de integración de informes"}


# 🚀 Ejecución principal
if __name__ == "__main__":
    input_dir = "app/uploads"
    output_file = "app/output/tabla_contenido_agente_v1.docx"
    agente_toc = crear_agente_toc()

    task_extraer_headings = Task(
        description="Extraer los encabezados numerados de los documentos Word en el directorio proporcionado.",
        agent=agente_toc,
        tools=[extraer_headings_desde_docx],
        function="extraer_headings_desde_docx",
        function_args={"input_dir": input_dir},
        output_key="headings",
        expected_output="Lista de encabezados extraídos con numeración y niveles.",
        auto_execute=True,  # 👈 IMPORTANTE
    )

    task_generar_toc = Task(
        description="Generar un documento Word con la tabla de contenido a partir de los encabezados extraídos.",
        agent=agente_toc,
        tools=[crear_doc_tabla_contenido],
        function="crear_doc_tabla_contenido",
        function_args={
            "headings": "{{headings}}",
            "output_file": output_file,
        },
        expected_output=f"Documento Word generado correctamente en {output_file}.",
        auto_execute=True,  # 👈 TAMBIÉN AQUÍ
    )

    crew = Crew(
        agents=[agente_toc],
        tasks=[task_extraer_headings, task_generar_toc],
        verbose=True,
    )

    resultado = crew.kickoff()
    print("\n🎉 Resultado final:", resultado)
