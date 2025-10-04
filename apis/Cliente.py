"""
API de Cliente - Endpoints para gestión de cliente
"""

from typing import List
from uuid import UUID

from crud.Cliente_crud import ClienteCRUD
from database.config import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import ClienteCreate, ClienteResponse, ClienteUpdate, RespuestaAPI
from sqlalchemy.orm import Session

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("/{id_biblioteca}", response_model=List[ClienteResponse])
async def obtener_clientes(
    id_biblioteca: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Obtener todos los clientes de una biblioteca.

    Args:
        id_biblioteca (UUID): ID de la biblioteca.
        skip (int, opcional): Número de registros a omitir. Default 0.
        limit (int, opcional): Número máximo de registros a retornar. Default 100.
        db (Session): Sesión de base de datos.

    Returns:
        List[ClienteResponse]: Lista de clientes registrados en la biblioteca.
    """
    try:
        cliente_crud = ClienteCRUD(db)
        clientes = cliente_crud.obtener_clientes(id_biblioteca, skip=skip, limit=limit)
        return clientes

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener clientes: {str(e)}",
        )


@router.get("/{id_biblioteca}/cliente/{codigo}", response_model=ClienteResponse)
async def obtener_cliente(
    codigo: UUID, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    """
    Obtener un cliente específico por su código.

    Args:
        codigo (UUID): ID del cliente.
        id_biblioteca (UUID): ID de la biblioteca.
        db (Session): Sesión de base de datos.

    Returns:
        ClienteResponse: Datos del cliente encontrado.
    """
    try:
        cliente_crud = ClienteCRUD(db)
        cliente = cliente_crud.obtener_cliente(codigo, id_biblioteca)
        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
            )
        return cliente

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cliente: {str(e)}",
        )


@router.get("/{id_biblioteca}/nombre/{nombre}", response_model=List[ClienteResponse])
async def obtener_clientes_por_nombre(
    nombre: str, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    """
    Buscar clientes por nombre dentro de una biblioteca.

    Args:
        nombre (str): Nombre del cliente o parte del nombre.
        id_biblioteca (UUID): ID de la biblioteca.
        db (Session): Sesión de base de datos.

    Returns:
        List[ClienteResponse]: Lista de clientes coincidentes.
    """
    try:
        cliente_crud = ClienteCRUD(db)
        clientes = cliente_crud.obtener_clientes_por_nombre(nombre, id_biblioteca)
        return clientes

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar clientes por nombre: {str(e)}",
        )


@router.get(
    "/{id_biblioteca}/tipo/{tipo_cliente}", response_model=List[ClienteResponse]
)
async def obtener_clientes_por_tipo(
    tipo_cliente: str, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    """
    Buscar clientes por tipo de cliente (ej. estudiante, docente, externo).

    Args:
        tipo_cliente (str): Tipo de cliente.
        id_biblioteca (UUID): ID de la biblioteca.
        db (Session): Sesión de base de datos.

    Returns:
        List[ClienteResponse]: Lista de clientes con el tipo especificado.
    """
    try:
        cliente_crud = ClienteCRUD(db)
        clientes = cliente_crud.obtener_clientes_por_tipo_cliente(
            tipo_cliente, id_biblioteca
        )
        return clientes

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar clientes por tipo: {str(e)}",
        )


@router.get(
    "/{id_biblioteca}/detalle/{detalle_tipo}", response_model=List[ClienteResponse]
)
async def obtener_clientes_por_detalle(
    detalle_tipo: str, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    """
    Buscar clientes según el detalle del tipo de cliente.

    Args:
        detalle_tipo (str): Detalle del tipo de cliente (ej. pregrado, posgrado).
        id_biblioteca (UUID): ID de la biblioteca.
        db (Session): Sesión de base de datos.

    Returns:
        List[ClienteResponse]: Lista de clientes que cumplen con el detalle.
    """
    try:
        cliente_crud = ClienteCRUD(db)
        clientes = cliente_crud.obtener_clientes_por_detalle_tipo(
            detalle_tipo, id_biblioteca
        )
        return clientes

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar clientes por detalle: {str(e)}",
        )


@router.get("/{id_biblioteca}/vetado/{vetado}", response_model=List[ClienteResponse])
async def obtener_clientes_por_vetado(
    vetado: bool, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    """
    Buscar clientes por estado de veto.

    Args:
        vetado (bool): Estado de veto (True si está vetado).
        id_biblioteca (UUID): ID de la biblioteca.
        db (Session): Sesión de base de datos.

    Returns:
        List[ClienteResponse]: Lista de clientes filtrados por su estado de veto.
    """
    try:
        cliente_crud = ClienteCRUD(db)
        clientes = cliente_crud.obtener_clientes_por_vetado(vetado, id_biblioteca)
        return clientes

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar clientes por estado de veto: {str(e)}",
        )


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def crear_cliente(cliente_data: ClienteCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo cliente en la biblioteca.

    Args:
        cliente_data (ClienteCreate): Datos del cliente a registrar.
        db (Session): Sesión de base de datos.

    Returns:
        ClienteResponse: Cliente creado exitosamente.
    """
    try:
        cliente_crud = ClienteCRUD(db)
        cliente = cliente_crud.crear_cliente(
            nombre=cliente_data.nombre,
            tipo_cliente=cliente_data.tipo_cliente,
            detalle_tipo=cliente_data.detalle_tipo,
            id_biblioteca=cliente_data.id_biblioteca,
        )
        return cliente

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear cliente: {str(e)}",
        )


@router.put("/{id_biblioteca}/cliente/{codigo}", response_model=ClienteResponse)
async def actualizar_cliente(
    codigo: UUID,
    id_biblioteca: UUID,
    cliente_data: ClienteUpdate,
    db: Session = Depends(get_db),
):
    """
    Actualizar la información de un cliente existente.

    Args:
        codigo (UUID): ID del cliente.
        id_biblioteca (UUID): ID de la biblioteca.
        cliente_data (ClienteUpdate): Campos a actualizar.
        db (Session): Sesión de base de datos.

    Returns:
        ClienteResponse: Cliente actualizado.
    """
    try:
        cliente_crud = ClienteCRUD(db)

        cliente_existente = cliente_crud.obtener_cliente(codigo, id_biblioteca)
        if not cliente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
            )

        campos_actualizacion = {
            k: v
            for k, v in cliente_data.dict().items()
            if v is not None and k != "id_biblioteca"
        }

        cliente_actualizado = cliente_crud.actualizar_cliente(
            codigo, id_biblioteca, **campos_actualizacion
        )
        return cliente_actualizado

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cliente: {str(e)}",
        )


@router.delete("/{id_biblioteca}/cliente/{codigo}", response_model=RespuestaAPI)
async def eliminar_cliente(
    codigo: UUID, id_biblioteca: UUID, db: Session = Depends(get_db)
):
    """
    Eliminar un cliente de la biblioteca.

    Args:
        codigo (UUID): ID del cliente.
        id_biblioteca (UUID): ID de la biblioteca.
        db (Session): Sesión de base de datos.

    Returns:
        RespuestaAPI: Mensaje de éxito si la eliminación fue correcta.
    """
    try:
        cliente_crud = ClienteCRUD(db)

        cliente_existente = cliente_crud.obtener_cliente(codigo, id_biblioteca)
        if not cliente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
            )

        eliminado = cliente_crud.eliminar_cliente(codigo, id_biblioteca)
        if eliminado:
            return RespuestaAPI(mensaje="Cliente eliminado exitosamente", exito=True)
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al eliminar cliente",
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar cliente: {str(e)}",
        )
