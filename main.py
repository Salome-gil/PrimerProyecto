"""
Sistema de Gestión Bibliotecaria - API principal con configuración de rutas y middleware
"""

import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.config import create_tables
from apis import (
    auth,
    Biblioteca,
    Categoria,
    Cliente,
    Material_Bibliografico,
    Prestamo,
    Reserva,
    Sancion,
    Sede,
    Usuario,
)

app = FastAPI(
    title="Sistema de Gestión Bibliotecaria",
    description="API REST para gestión de usuario autenticados, categoría, clientes, material bibliográfico, préstamos, reservas y sanciones",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(Biblioteca.router)
app.include_router(Categoria.router)
app.include_router(Cliente.router)
app.include_router(Material_Bibliografico.router)
app.include_router(Prestamo.router)
app.include_router(Reserva.router)
app.include_router(Sancion.router)
app.include_router(Sede.router)
app.include_router(Usuario.router)


@app.on_event("startup")
async def startup_event():
    """
    Evento de inicio de la aplicación.

    Configura la base de datos y prepara el sistema para iniciar.
    """
    print("Iniciando Sistema de Gestión Bibliotecario...")
    print("Configurando base de datos...")
    create_tables()
    print("Sistema listo para usar.")
    print("Documentación disponible en: http://localhost:8000/docs")


@app.get("/", tags=["raíz"])
async def root():
    """
    Endpoint raíz que devuelve información básica de la API.

    Returns:
        dict: Mensaje de bienvenida, versión y enlaces de documentación y endpoints principales.
    """
    return {
        "mensaje": "Bienvenido al Sistema de Gestión Bibliotecario",
        "version": "1.0.0",
        "documentacion": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "autenticacion": "/auth",
            "Bibliotecas": "/bibliotecas",
            "Categorias": "/categorias",
            "Clientes": "/clientes",
            "Materiales Bibliograficos": "/materiales bibliograficos",
            "Préstamos": "/prestamos",
            "Reservas": "/reservas",
            "Sanciones": "/sanciones",
            "Sedes": "/sedes",
            "Usuarios": "/usuarios",
        },
    }


def main():
    """
    Función principal para ejecutar el servidor.

    Inicia la aplicación FastAPI con Uvicorn.
    """
    print("Iniciando servidor FastAPI...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")


if __name__ == "__main__":
    main()
