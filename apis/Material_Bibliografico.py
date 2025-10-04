"""
API de Material Bibliográfico - Endpoints para gestión de material bibliográfico
"""

from typing import List
from uuid import UUID

from crud.Material_Bibliografico_crud import MaterialBibliograficoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import (
    Material_BibliograficoCreate,
    Material_BibliograficoResponse,
    Material_BibliograficoUpdate,
    RespuestaAPI,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/materiales", tags=["materiales"])


@router.get("/{id_biblioteca}", response_model=List[Material_BibliograficoResponse])
async def obtener_materiales(
    id_biblioteca: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener todos los materiales de una biblioteca.

    Args:
        id_biblioteca (UUID): Identificador único de la biblioteca.
        skip (int, opcional): Número de registros a omitir. Por defecto 0.
        limit (int, opcional): Número máximo de registros a devolver. Por defecto 100.
        db (Session): Sesión de base de datos.

    Returns:
        List[Material_BibliograficoResponse]: Lista de materiales de la biblioteca.
    """
    try:
        material_crud = MaterialBibliograficoCRUD(db)
        materiales = material_crud.obtener_materiales(id_biblioteca, skip, limit)
        return materiales

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener materiales: {str(e)}",
        )


@router.get(
    "/{id_biblioteca}/material/{id_material}",
    response_model=Material_BibliograficoResponse,
)
async def obtener_material(
    id_material: UUID, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    """
    Obtener un material específico de una biblioteca.

    Args:
        id_material (UUID): Identificador único del material.
        id_biblioteca (UUID): Identificador único de la biblioteca.
        db (Session): Sesión de base de datos.

    Returns:
        Material_BibliograficoResponse: Información del material encontrado.
    """
    try:
        material_crud = MaterialBibliograficoCRUD(db)
        material = material_crud.obtener_material(id_material, id_biblioteca)
        if not material:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Material no encontrado"
            )
        return material

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener material: {str(e)}",
        )


@router.get(
    "/{id_biblioteca}/titulo/{titulo}",
    response_model=List[Material_BibliograficoResponse],
)
async def obtener_materiales_por_titulo(
    titulo: str, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    """
    Obtener materiales de una biblioteca por título.

    Args:
        titulo (str): Título del material.
        id_biblioteca (UUID): Identificador único de la biblioteca.
        db (Session): Sesión de base de datos.

    Returns:
        List[Material_BibliograficoResponse]: Lista de materiales encontrados.
    """
    try:
        material_crud = MaterialBibliograficoCRUD(db)
        materiales = material_crud.obtener_materiales_por_titulo(titulo, id_biblioteca)
        if not materiales:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Material no encontrado"
            )
        return materiales

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar materiales por título: {str(e)}",
        )


@router.get(
    "/{id_biblioteca}/autor/{autor}",
    response_model=List[Material_BibliograficoResponse],
)
async def obtener_materiales_por_autor(
    autor: str, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    """
    Obtener materiales de una biblioteca por autor.

    Args:
        autor (str): Nombre del autor.
        id_biblioteca (UUID): Identificador único de la biblioteca.
        db (Session): Sesión de base de datos.

    Returns:
        List[Material_BibliograficoResponse]: Lista de materiales encontrados.
    """
    try:
        material_crud = MaterialBibliograficoCRUD(db)
        materiales = material_crud.obtener_materiales_por_autor(autor, id_biblioteca)
        if not materiales:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Material no encontrado"
            )
        return materiales

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar materiales por autor: {str(e)}",
        )


@router.get(
    "/{id_biblioteca}/estado/{estado}",
    response_model=List[Material_BibliograficoResponse],
)
async def obtener_materiales_por_estado(
    estado: str, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    """
    Obtener materiales de una biblioteca por estado.

    Args:
        estado (str): Estado del material (ejemplo: disponible, prestado).
        id_biblioteca (UUID): Identificador único de la biblioteca.
        db (Session): Sesión de base de datos.

    Returns:
        List[Material_BibliograficoResponse]: Lista de materiales encontrados.
    """
    try:
        material_crud = MaterialBibliograficoCRUD(db)
        materiales = material_crud.obtener_materiales_por_estado(estado, id_biblioteca)
        if not materiales:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Material no encontrado"
            )
        return materiales

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar materiales por estado: {str(e)}",
        )


@router.get(
    "/{id_biblioteca}/categoria/{id_categoria}",
    response_model=List[Material_BibliograficoResponse],
)
async def obtener_materiales_por_categoria(
    id_categoria: UUID, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    """
    Obtener materiales de una biblioteca por categoría.

    Args:
        id_categoria (UUID): Identificador único de la categoría.
        id_biblioteca (UUID): Identificador único de la biblioteca.
        db (Session): Sesión de base de datos.

    Returns:
        List[Material_BibliograficoResponse]: Lista de materiales encontrados.
    """
    try:
        material_crud = MaterialBibliograficoCRUD(db)
        materiales = material_crud.obtener_materiales_por_categoria(
            id_categoria, id_biblioteca
        )
        if not materiales:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Material no encontrado"
            )
        return materiales

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener materiales por categoría: {str(e)}",
        )


@router.post(
    "/",
    response_model=Material_BibliograficoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def crear_material(
    material_data: Material_BibliograficoCreate, db: Session = Depends(get_db)
):
    """
    Crear un nuevo material en una biblioteca.

    Args:
        material_data (Material_BibliograficoCreate): Datos del material a crear.
        db (Session): Sesión de base de datos.

    Returns:
        Material_BibliograficoResponse: Información del material creado.
    """
    try:
        material_crud = MaterialBibliograficoCRUD(db)
        material = material_crud.crear_material(
            id_biblioteca=material_data.id_biblioteca,
            titulo=material_data.titulo,
            autor=material_data.autor,
            estado=material_data.estado,
            id_sede=material_data.id_sede,
            id_categoria=material_data.id_categoria,
        )
        return material

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear material: {str(e)}",
        )


@router.put(
    "/{id_biblioteca}/{id_material}", response_model=Material_BibliograficoResponse
)
async def actualizar_material(
    id_material: UUID,
    id_biblioteca: UUID,
    material_data: Material_BibliograficoUpdate,
    db: Session = Depends(get_db),
):
    """
    Actualizar los datos de un material en una biblioteca.

    Args:
        id_material (UUID): Identificador único del material.
        id_biblioteca (UUID): Identificador único de la biblioteca.
        material_data (Material_BibliograficoUpdate): Datos a actualizar en el material.
        db (Session): Sesión de base de datos.

    Returns:
        Material_BibliograficoResponse: Material actualizado.
    """
    try:
        material_crud = MaterialBibliograficoCRUD(db)

        material_existente = material_crud.obtener_material(id_material, id_biblioteca)
        if not material_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Material no encontrado"
            )

        campos_actualizacion = {
            k: v
            for k, v in material_data.dict().items()
            if v is not None and k != "id_biblioteca"
        }

        if not campos_actualizacion:
            return material_existente

        material_actualizado = material_crud.actualizar_material(
            id_material, id_biblioteca, **campos_actualizacion
        )
        return material_actualizado

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar material: {str(e)}",
        )


@router.delete("/{id_biblioteca}/{id_material}", response_model=RespuestaAPI)
async def eliminar_material(
    id_material: UUID, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    """
    Eliminar un material de una biblioteca.

    Args:
        id_material (UUID): Identificador único del material.
        id_biblioteca (UUID): Identificador único de la biblioteca.
        db (Session): Sesión de base de datos.

    Returns:
        RespuestaAPI: Mensaje de confirmación y estado de la operación.
    """
    try:
        material_crud = MaterialBibliograficoCRUD(db)

        material_existente = material_crud.obtener_material(id_material, id_biblioteca)
        if not material_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Material no encontrado"
            )

        eliminado = material_crud.eliminar_material(id_material, id_biblioteca)
        if eliminado:
            return RespuestaAPI(mensaje="Material eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar material",
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar material: {str(e)}",
        )
