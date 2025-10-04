"""
API de Reserva - Endpoints para gestión de reservas
"""

from typing import List
from uuid import UUID

from crud.Reserva_crud import ReservaCrud
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ReservaCreate, ReservaResponse, ReservaUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/reservas", tags=["reservas"])


@router.get("/{id_biblioteca}", response_model=List[ReservaResponse])
async def obtener_reservas(
    id_biblioteca: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    try:
        Reserva_crud = ReservaCrud(db)
        reservas = Reserva_crud.obtener_reservas(id_biblioteca, skip=skip, limit=limit)
        return reservas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la reserva: {str(e)}",
        )


@router.get("/{id_biblioteca}/reserva/{id_resvera}", response_model=ReservaResponse)
async def obtener_reserva(
    id_reserva: UUID, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    """Obtener una  reserva por ID."""
    try:
        Reserva_crud = ReservaCrud(db)
        reserva = Reserva_crud.obtener_reserva(id_reserva, id_biblioteca)
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada"
            )
        return reserva
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la reserva: {str(e)}",
        )


@router.get(
    "/{id_biblioteca}/nombre/{cod_cliente}", response_model=List[ReservaResponse]
)
async def obtener_reserva_por_cliente(
    cod_cliente: UUID, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    """Obtener una reserva por el id del cliente."""
    try:
        Reserva_crud = ReservaCrud(db)
        reserva = Reserva_crud.obtener_reservas_por_cliente(cod_cliente, id_biblioteca)
        if not reserva:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada"
            )
        return reserva
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la reserva: {str(e)}",
        )


@router.post("/", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
async def crear_reserva(reserva_data: ReservaCreate, db: Session = Depends(get_db)):
    """Crear una nueva reserva."""
    try:
        Reserva_crud = ReservaCrud(db)
        reserva = Reserva_crud.crear_reserva(
            id_material=reserva_data.id_material,
            estado=reserva_data.estado,
            fecha_reserva=reserva_data.fecha_reserva,
            cod_cliente=reserva_data.cod_cliente,
            id_biblioteca=reserva_data.id_biblioteca,
        )
        return reserva
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la reserva: {str(e)}",
        )


@router.put("/{id_biblioteca}/{id_reserva}", response_model=ReservaResponse)
async def actualizar_reserva(
    id_reserva: UUID,
    id_biblioteca: UUID,
    reserva_data: ReservaUpdate,
    db: Session = Depends(get_db),
):
    try:
        Reserva_crud = ReservaCrud(db)

        # Verificar que la reserva existe
        reserva_existente = Reserva_crud.obtener_reserva(id_reserva, id_biblioteca)
        if not reserva_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada"
            )

        # Filtrar campos None para actualización
        campos_actualizacion = {
            k: v
            for k, v in reserva_data.dict().items()
            if v is not None and k != "id_biblioteca"
        }

        if not campos_actualizacion:
            return reserva_existente

        reserva_actualizada = Reserva_crud.actualizar_reserva(
            id_reserva, id_biblioteca, **campos_actualizacion
        )
        return reserva_actualizada
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar la reserva: {str(e)}",
        )


@router.delete("/{id_biblioteca}/{id_reserva}", response_model=RespuestaAPI)
async def eliminar_reserva(
    id_reserva: UUID, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    """Eliminar una reserva."""
    try:
        Reserva_crud = ReservaCrud(db)

        # Verificar que la reserva existe
        reserva_existente = Reserva_crud.obtener_reserva(id_reserva, id_biblioteca)
        if not reserva_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Reserva no encontrada"
            )

        eliminada = Reserva_crud.eliminar_reserva(id_reserva, id_biblioteca)
        if eliminada:
            return RespuestaAPI(mensaje="Reserva eliminada exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar la reserva",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar la reserva: {str(e)}",
        )
