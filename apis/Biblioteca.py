"""
API de Biblioteca - Endpoints para gestión de biblioteca
"""

from typing import List
from uuid import UUID

from crud.Biblioteca_crud import BibliotecaCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import BibliotecaCreate, BibliotecaResponse, BibliotecaUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/bibliotecas", tags=["bibliotecas"])


@router.get("/", response_model=List[BibliotecaResponse])
async def obtener_bibliotecas(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener todas las bibliotecas registradas.

    Args:
        skip (int, opcional): Número de registros a omitir. Por defecto es 0.
        limit (int, opcional): Cantidad máxima de registros a devolver. Por defecto es 100.
        db (Session): Sesión de base de datos inyectada por FastAPI.

    Returns:
        List[BibliotecaResponse]: Lista de bibliotecas disponibles.
    """
    try:
        biblioteca_crud = BibliotecaCRUD(db)
        bibliotecas = biblioteca_crud.obtener_bibliotecas(skip=skip, limit=limit)
        return bibliotecas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener bibliotecas: {str(e)}",
        )


@router.get("/{id_biblioteca}", response_model=BibliotecaResponse)
async def obtener_biblioteca(id_biblioteca: UUID, db: Session = Depends(get_db)):
    """
    Obtener una biblioteca específica por su ID.

    Args:
        id_biblioteca (UUID): Identificador único de la biblioteca.
        db (Session): Sesión de base de datos.

    Returns:
        BibliotecaResponse: Datos de la biblioteca encontrada.
    """
    try:
        biblioteca_crud = BibliotecaCRUD(db)
        biblioteca = biblioteca_crud.obtener_biblioteca(id_biblioteca)
        if not biblioteca:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Biblioteca no encontrada"
            )
        return biblioteca
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener biblioteca: {str(e)}",
        )


@router.get("/nombre/{nombre}", response_model=BibliotecaResponse)
async def obtener_biblioteca_por_nombre(nombre: str, db: Session = Depends(get_db)):
    """
    Obtener una biblioteca por su nombre.

    Args:
        nombre (str): Nombre de la biblioteca.
        db (Session): Sesión de base de datos.

    Returns:
        BibliotecaResponse: Información de la biblioteca encontrada.
    """
    try:
        biblioteca_crud = BibliotecaCRUD(db)
        biblioteca = biblioteca_crud.obtener_biblioteca_por_nombre(nombre)
        if not biblioteca:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Biblioteca no encontrada"
            )
        return biblioteca
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener biblioteca: {str(e)}",
        )


@router.get("/sede/{id_sede}", response_model=BibliotecaResponse)
async def obtener_biblioteca_por_sede(id_sede: UUID, db: Session = Depends(get_db)):
    """
    Obtener una biblioteca asociada a una sede.

    Args:
        id_sede (UUID): Identificador único de la sede.
        db (Session): Sesión de base de datos.

    Returns:
        BibliotecaResponse: Información de la biblioteca encontrada.
    """
    try:
        biblioteca_crud = BibliotecaCRUD(db)
        biblioteca = biblioteca_crud.obtener_biblioteca_por_sede(id_sede)
        if not biblioteca:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Biblioteca no encontrada"
            )
        return biblioteca
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener biblioteca por sede: {str(e)}",
        )


@router.post(
    "/", response_model=BibliotecaResponse, status_code=status.HTTP_201_CREATED
)
async def crear_biblioteca(
    biblioteca_data: BibliotecaCreate, db: Session = Depends(get_db)
):
    """
    Crear una nueva biblioteca.

    Args:
        biblioteca_data (BibliotecaCreate): Datos necesarios para crear la biblioteca.
        db (Session): Sesión de base de datos.

    Returns:
        BibliotecaResponse: Información de la biblioteca creada.
    """
    try:
        biblioteca_crud = BibliotecaCRUD(db)
        biblioteca = biblioteca_crud.crear_biblioteca(
            nombre=biblioteca_data.nombre, id_sede=biblioteca_data.id_sede
        )
        return biblioteca
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear biblioteca: {str(e)}",
        )


@router.put("/{id_biblioteca}", response_model=BibliotecaResponse)
async def actualizar_biblioteca(
    id_biblioteca: UUID,
    biblioteca_data: BibliotecaUpdate,
    db: Session = Depends(get_db),
):
    """
    Actualizar los datos de una biblioteca existente.

    Args:
        id_biblioteca (UUID): Identificador de la biblioteca a actualizar.
        biblioteca_data (BibliotecaUpdate): Campos a modificar.
        db (Session): Sesión de base de datos.

    Returns:
        BibliotecaResponse: Biblioteca con los datos actualizados.
    """
    try:
        biblioteca_crud = BibliotecaCRUD(db)

        biblioteca_existente = biblioteca_crud.obtener_biblioteca(id_biblioteca)
        if not biblioteca_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Biblioteca no encontrada"
            )

        campos_actualizacion = {
            k: v for k, v in biblioteca_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return biblioteca_existente

        biblioteca_actualizada = biblioteca_crud.actualizar_biblioteca(
            id_biblioteca, **campos_actualizacion
        )
        return biblioteca_actualizada

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar biblioteca: {str(e)}",
        )


@router.delete("/{id_biblioteca}", response_model=RespuestaAPI)
async def eliminar_biblioteca(id_biblioteca: UUID, db: Session = Depends(get_db)):
    """
    Eliminar una biblioteca de la base de datos.

    Args:
        id_biblioteca (UUID): Identificador único de la biblioteca a eliminar.
        db (Session): Sesión de base de datos.

    Returns:
        RespuestaAPI: Mensaje de confirmación y estado de la operación.
    """
    try:
        biblioteca_crud = BibliotecaCRUD(db)

        biblioteca_existente = biblioteca_crud.obtener_biblioteca(id_biblioteca)
        if not biblioteca_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Biblioteca no encontrada"
            )

        eliminado = biblioteca_crud.eliminar_biblioteca(id_biblioteca)
        if eliminado:
            return RespuestaAPI(mensaje="Biblioteca eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar biblioteca",
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar biblioteca: {str(e)}",
        )
