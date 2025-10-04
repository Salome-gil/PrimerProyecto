"""
API de Prestamo - Endpoints para gestión de prestamos
"""

from typing import List
from uuid import UUID

from crud.Prestamo_crud import PrestamoCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import PrestamoCreate, PrestamoResponse, PrestamoUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/prestamos", tags=["prestamos"])


@router.get("/{id_biblioteca}", response_model=List[PrestamoResponse])
async def obtener_prestamos(
    id_biblioteca: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    try:
        Prestamo_crud = PrestamoCRUD(db)
        prestamos = Prestamo_crud.obtener_prestamos(
            id_biblioteca, skip=skip, limit=limit
        )
        return prestamos

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el prestamo: {str(e)}",
        )


@router.get("/{id_biblioteca}/prestamo/{prestamo_id}", response_model=PrestamoResponse)
async def obtener_prestamo(
    prestamo_id: UUID, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    try:
        Prestamo_crud = PrestamoCRUD(db)
        prestamo = Prestamo_crud.obtener_prestamo(prestamo_id, id_biblioteca)
        if not prestamo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Prestamo no encontrado"
            )
        return prestamo

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el prestamo: {str(e)}",
        )


@router.get("/{id_biblioteca}/cliente/{cod_cliente}", response_model=List[PrestamoResponse])
async def obtener_prestamos_por_cliente(
    id_biblioteca: UUID, cod_cliente: UUID, db: Session = Depends(get_db)
):
    try:
        Prestamo_crud = PrestamoCRUD(db)
        prestamo = Prestamo_crud.obtener_prestamos_por_cliente(
            cod_cliente, id_biblioteca
        )
        if not prestamo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Prestamo no encontrado"
            )
        return prestamo

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el prestamo: {str(e)}",
        )


@router.post("/", response_model=PrestamoResponse, status_code=status.HTTP_201_CREATED)
async def crear_prestamo(prestamo_data: PrestamoCreate, db: Session = Depends(get_db)):
    try:
        Prestamo_crud = PrestamoCRUD(db)
        prestamo = Prestamo_crud.crear_prestamo(
            fecha_prestamo=prestamo_data.fecha_prestamo,
            fecha_entrega=prestamo_data.fecha_entrega,
            id_material=prestamo_data.id_material,
            cod_cliente=prestamo_data.cod_cliente,
            id_biblioteca=prestamo_data.id_biblioteca,
        )
        return prestamo

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el prestamo: {str(e)}",
        )


@router.put("/{id_biblioteca}/{id_prestamo}", response_model=PrestamoResponse)
async def actualizar_prestamo(
    id_prestamo: UUID,
    id_biblioteca: UUID,
    prestamo_data: PrestamoUpdate,
    db: Session = Depends(get_db),
):
    try:
        Prestamo_cud = PrestamoCRUD(db)

        prestamo_existente = Prestamo_cud.obtener_prestamo(id_prestamo, id_biblioteca)
        if not prestamo_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Prestamo no encontrado"
            )

        campos_actualizacion = {
            k: v
            for k, v in prestamo_data.dict().items()
            if v is not None and k != "id_biblioteca"
        }

        if not campos_actualizacion:
            return prestamo_existente

        prestamo_actualizado = Prestamo_cud.actualizar_prestamo(
            id_prestamo, id_biblioteca, **campos_actualizacion
        )
        return prestamo_actualizado

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el prestamo: {str(e)}",
        )


@router.delete("/{id_biblioteca}/{id_prestamo}", response_model=RespuestaAPI)
async def elimiar_prestamo(
    id_biblioteca: UUID, id_prestamo: UUID, db: Session = Depends(get_db)
):
    try:
        Prestamo_crud = PrestamoCRUD(db)

        prestamo_existente = Prestamo_crud.obtener_prestamo(id_prestamo, id_biblioteca)
        if not prestamo_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Prestamo no encontrado"
            )

        eliminada = Prestamo_crud.eliminar_prestamo(id_prestamo, id_biblioteca)
        if eliminada:
            return RespuestaAPI(mensaje="Prestamo eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar el prestamo",
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el prestamo: {str(e)}",
        )
