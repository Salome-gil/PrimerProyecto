"""
API de sancion - Endpoints para gestión de sanciones
"""

from typing import List
from uuid import UUID

from crud.Sancion_crud import SancionCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import SancionCreate, SancionResponse, SancionUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/sanciones", tags=["sanciones"])


@router.get("/{id_biblioteca}", response_model=List[SancionResponse])
async def obtener_sanciones(
    id_biblioteca: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    try:
        Sancion_crud = SancionCRUD(db)
        sanciones = Sancion_crud.obtener_sanciones(
            id_biblioteca, skip=skip, limit=limit
        )
        return sanciones
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la sancion: {str(e)}",
        )


@router.get("/{id_biblioteca}/sancion/{id_sancion}", response_model=SancionResponse)
async def obtener_sancion(
    id_sancion: UUID, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    try:
        Sancion_crud = SancionCRUD(db)
        sancion = Sancion_crud.obtener_sancion(id_sancion, id_biblioteca)
        if not sancion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sancion no encontrada"
            )
        return sancion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la sancion: {str(e)}",
        )


@router.get("/{id_biblioteca}/nombre/{cod_cliente}", response_model=List[SancionResponse])
async def obtener_sancion_por_cliente(
    cod_cliente: UUID, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    try:
        Sancion_crud = SancionCRUD(db)
        sancion = Sancion_crud.obtener_sanciones_por_cliente(cod_cliente, id_biblioteca)
        if not sancion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sancion no encontrada"
            )
        return sancion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la sancion: {str(e)}",
        )


@router.post("/", response_model=SancionResponse, status_code=status.HTTP_201_CREATED)
async def crear_sancion(sancion_data: SancionCreate, db: Session = Depends(get_db)):
    try:
        Sancion_crud = SancionCRUD(db)
        sancion = Sancion_crud.crear_sancion(
            monto=sancion_data.monto,
            fecha_sancion=sancion_data.fecha_sancion,
            cod_cliente=sancion_data.cod_cliente,
            id_biblioteca=sancion_data.id_biblioteca,
        )
        return sancion
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la sancion: {str(e)}",
        )


@router.put("/{id_biblioteca}/{id_sancion}", response_model=SancionResponse)
async def actualizar_sancion(
    id_sancion: UUID,
    id_biblioteca: UUID,
    sancion_data: SancionUpdate,
    db: Session = Depends(get_db),
):
    try:
        Sancion_crud = SancionCRUD(db)

        sancion_existente = Sancion_crud.obtener_sancion(id_sancion, id_biblioteca)
        if not sancion_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sancion no encontrada"
            )

        campos_actualizacion = {
            k: v
            for k, v in sancion_data.dict().items()
            if v is not None and k != "id_biblioteca"
        }

        if not campos_actualizacion:
            return sancion_existente

        sancion_actualizada = Sancion_crud.actualizar_sancion(
            id_sancion, id_biblioteca, **campos_actualizacion
        )
        return sancion_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la sancion: {str(e)}",
        )


@router.delete("/{id_biblioteca}/{id_sancion}", response_model=RespuestaAPI)
async def eliminar_sancion(
    id_sancion: UUID, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    try:
        Sancion_crud = SancionCRUD(db)

        sancion_existente = Sancion_crud.obtener_sancion(id_sancion, id_biblioteca)
        if not sancion_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sancion no encontrada"
            )

        eliminada = Sancion_crud.eliminar_sancion(id_sancion, id_biblioteca)
        if eliminada:
            return RespuestaAPI(mensaje="Sancion eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar la sancion",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la sancion: {str(e)}",
        )
