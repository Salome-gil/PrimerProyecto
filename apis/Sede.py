"""
API de sede - Endpoints para gestión de sedes
"""

from typing import List
from uuid import UUID

from crud.Sede_crud import SedeCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import SedeCreate, SedeResponse, SedeUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/sedes", tags=["sedes"])


@router.get("/", response_model=List[SedeResponse])
async def obtener_sedes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener todas las sedes con paginación."""
    try:
        Sede_crud = SedeCRUD(db)
        sedes = Sede_crud.obtener_sedes(skip=skip, limit=limit)
        return sedes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las sedes: {str(e)}",
        )


@router.get("/sede/{id_sede}", response_model=SedeResponse)
async def obtener_sede(id_sede: UUID, db: Session = Depends(get_db)):
    """Obtener una  sede por ID."""
    try:
        Sede_crud = SedeCRUD(db)
        sede = Sede_crud.obtener_sede(id_sede)
        if not sede:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sede no encontrada"
            )
        return sede
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la sede: {str(e)}",
        )


@router.get("/nombre/{nombre}", response_model=SedeResponse)
async def obtener_sede_por_nombre(nombre: str, db: Session = Depends(get_db)):
    """Obtener una sede por el nombre."""
    try:
        Sede_crud = SedeCRUD(db)
        sede = Sede_crud.obtener_sede_por_nombre(nombre)
        if not sede:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sede no encontrada"
            )
        return sede
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la sede: {str(e)}",
        )


@router.post("/", response_model=SedeResponse, status_code=status.HTTP_201_CREATED)
async def crear_sede(sede_data: SedeCreate, db: Session = Depends(get_db)):
    """Crear una nueva sede."""
    try:
        Sede_crud = SedeCRUD(db)
        sede = Sede_crud.crear_sede(
            nombre=sede_data.nombre, direccion=sede_data.direccion
        )
        return sede
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la sede: {str(e)}",
        )


@router.put("/{id_sede}", response_model=SedeResponse)
async def actualizar_sede(
    id_sede: UUID, sede_data: SedeUpdate, db: Session = Depends(get_db)
):
    """Actualizar una sede existente."""
    try:
        Sede_crud = SedeCRUD(db)

        # Verificar que la sancion existe
        sede_existente = Sede_crud.obtener_sede(id_sede)
        if not sede_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sede no encontrada"
            )

        # Filtrar campos None para actualización
        campos_actualizacion = {
            k: v for k, v in sede_data.dict().items() if v is not None
        }

        if not campos_actualizacion:
            return sede_existente

        sede_actualizada = Sede_crud.actualizar_sede(id_sede, **campos_actualizacion)
        return sede_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la sede: {str(e)}",
        )


@router.delete("/{id_sede}", response_model=RespuestaAPI)
async def eliminar_sede(id_sede: UUID, db: Session = Depends(get_db)):
    """Eliminar una sede."""
    try:
        Sede_crud = SedeCRUD(db)

        # Verificar que la sede existe
        sede_existente = Sede_crud.obtener_sede(id_sede)
        if not sede_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sede no encontrada"
            )

        eliminada = Sede_crud.eliminar_sede(id_sede)
        if eliminada:
            return RespuestaAPI(mensaje="Sede eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar la sede",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la sasedencion: {str(e)}",
        )
