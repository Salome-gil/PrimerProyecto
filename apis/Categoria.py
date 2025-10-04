"""
API de Categoria - Endpoints para gestión de categoria
"""

from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud.Categoria_crud import CategoriaCRUD
from database.config import get_db
from schemas import CategoriaCreate, CategoriaUpdate, CategoriaResponse, RespuestaAPI

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("/{id_biblioteca}", response_model=List[CategoriaResponse])
async def obtener_categorias(
    id_biblioteca: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener todas las categorías de una biblioteca.

    Args:
        id_biblioteca (UUID): Identificador único de la biblioteca.
        skip (int, opcional): Número de registros a omitir. Por defecto 0.
        limit (int, opcional): Número máximo de registros a devolver. Por defecto 100.
        db (Session): Sesión de base de datos.

    Returns:
        List[CategoriaResponse]: Lista de categorías asociadas a la biblioteca.
    """
    try:
        categoria_crud = CategoriaCRUD(db)
        categorias = categoria_crud.obtener_categorias(id_biblioteca, skip, limit)
        return categorias
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener categorías: {str(e)}",
        )


@router.get(
    "/{id_biblioteca}/categoria/{id_categoria}",
    response_model=CategoriaResponse,
)
async def obtener_categoria(
    id_biblioteca: UUID, id_categoria: UUID, db: Session = Depends(get_db)
):
    """
    Obtener una categoría específica de una biblioteca.

    Args:
        id_biblioteca (UUID): Identificador único de la biblioteca.
        id_categoria (UUID): Identificador único de la categoría.
        db (Session): Sesión de base de datos.

    Returns:
        CategoriaResponse: Información de la categoría encontrada.
    """
    try:
        categoria_crud = CategoriaCRUD(db)
        categoria = categoria_crud.obtener_categoria(id_categoria, id_biblioteca)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
            )
        return categoria

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener categoría: {str(e)}",
        )


@router.get("/{id_biblioteca}/nombre/{nombre}", response_model=CategoriaResponse)
async def obtener_categoria_por_nombre(
    nombre: str, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    """
    Obtener una categoría de una biblioteca por su nombre.

    Args:
        nombre (str): Nombre de la categoría.
        id_biblioteca (UUID): Identificador de la biblioteca a la que pertenece.
        db (Session): Sesión de base de datos.

    Returns:
        CategoriaResponse: Información de la categoría encontrada.
    """
    try:
        crud = CategoriaCRUD(db)
        categoria = crud.obtener_categoria_por_nombre(nombre, id_biblioteca)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
            )
        return categoria

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar categoría: {str(e)}",
        )


@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
async def crear_categoria(
    categoria_data: CategoriaCreate, db: Session = Depends(get_db)
):
    """
    Crear una nueva categoría dentro de una biblioteca.

    Args:
        categoria_data (CategoriaCreate): Datos de la categoría a crear.
        db (Session): Sesión de base de datos.

    Returns:
        CategoriaResponse: Información de la categoría creada.
    """
    try:
        crud = CategoriaCRUD(db)
        return crud.crear_categoria(
            id_biblioteca=categoria_data.id_biblioteca,
            nombre=categoria_data.nombre,
            descripcion=categoria_data.descripcion,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear categoría: {str(e)}",
        )


@router.put(
    "/{id_biblioteca}/categoria/{id_categoria}",
    response_model=CategoriaResponse,
)
async def actualizar_categoria(
    id_biblioteca: UUID,
    id_categoria: UUID,
    categoria_data: CategoriaUpdate,
    db: Session = Depends(get_db),
):
    """
    Actualizar los datos de una categoría de una biblioteca.

    Args:
        id_biblioteca (UUID): Identificador único de la biblioteca.
        id_categoria (UUID): Identificador único de la categoría a actualizar.
        categoria_data (CategoriaUpdate): Datos a actualizar en la categoría.
        db (Session): Sesión de base de datos.

    Returns:
        CategoriaResponse: Categoría con la información actualizada.
    """
    try:
        crud = CategoriaCRUD(db)

        categoria_existente = crud.obtener_categoria(id_categoria, id_biblioteca)
        if not categoria_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
            )

        campos_actualizacion = {
            k: v
            for k, v in categoria_data.dict().items()
            if v is not None and k != "id_biblioteca"
        }

        categoria_actualizada = crud.actualizar_categoria(
            id_categoria, id_biblioteca, **campos_actualizacion
        )
        return categoria_actualizada

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar categoría: {str(e)}",
        )


@router.delete("/{id_biblioteca}/categoria/{id_categoria}", response_model=RespuestaAPI)
async def eliminar_categoria(
    id_biblioteca: UUID, id_categoria: UUID, db: Session = Depends(get_db)
):
    """
    Eliminar una categoría de una biblioteca.

    Args:
        id_biblioteca (UUID): Identificador único de la biblioteca.
        id_categoria (UUID): Identificador único de la categoría.
        db (Session): Sesión de base de datos.

    Returns:
        RespuestaAPI: Mensaje de confirmación y estado de la operación.
    """
    try:
        crud = CategoriaCRUD(db)

        categoria_existente = crud.obtener_categoria(id_categoria, id_biblioteca)
        if not categoria_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada"
            )

        eliminado = crud.eliminar_categoria(id_categoria, id_biblioteca)
        if eliminado:
            return RespuestaAPI(mensaje="Categoría eliminada exitosamente", exito=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar categoría",
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar categoría: {str(e)}",
        )
