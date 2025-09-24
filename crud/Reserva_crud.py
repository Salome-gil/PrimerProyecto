from datetime import date
from uuid import UUID
from typing import List, Optional
from entities.Reserva import Reserva
from sqlalchemy.orm import Session, joinedload

class ReservaCrud:
    """
    Clase para realizar operaciones CRUD sobre reservas en la base de datos.
    """

    def __init__(self, db: Session):
        """
        Inicializa el CRUD con una sesión de base de datos.

        Args:
            db (Session): Sesión de SQLAlchemy para interactuar con la base de datos.
        """
        self.db= db

    def crear_reserva(self, fecha_reserva: date, estado:str, id_material: UUID, cod_cliente: UUID, id_biblioteca: UUID, id_usuario_crea: UUID = None) -> Reserva:
        """
        Crea una nueva reserva en la base de datos.

        Args:
            fecha_reserva (date): Fecha de la reserva.
            estado (str): Estado inicial de la reserva.
            id_material (UUID): Identificador único del material.
            cod_cliente (UUID): Identificador único del cliente.
            id_biblioteca (UUID): Identificador único de la biblioteca.
            id_usuario_crea (UUID, opcional): Identificador del usuario que crea la reserva. 
                                              Si no se proporciona, se asigna un administrador.

        Returns:
            Reserva: Objeto de la reserva creada.
        """
        if not fecha_reserva:
            raise ValueError("La fecha de la reserva es obligatoria")

        if not estado or len(estado.strip()) == 0:
            raise ValueError("El estado de la reserva es obligatorio")
        if len(estado.strip()) > 50:
            raise ValueError("El estado no puede exceder 50 caracteres")

        if not id_material:
            raise ValueError("El material es obligatorio")
        if not cod_cliente:
            raise ValueError("El cliente es obligatorio")
        if not id_biblioteca:
            raise ValueError("La biblioteca es obligatoria")

        if id_usuario_crea is None:
            from entities.Usuario import Usuario
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError("No se encontró un usuario administrador para crear la reserva")
            id_usuario_crea = admin.id_usuario

        reserva= Reserva(
            fecha_reserva= fecha_reserva, 
            estado= estado.strip().lower(), 
            id_material= id_material, 
            cod_cliente= cod_cliente,
            id_biblioteca=id_biblioteca,
            id_usuario_crea= id_usuario_crea)
        
        self.db.add(reserva)
        self.db.commit()
        self.db.refresh(reserva)
        return reserva
    
    def obtener_reserva(self, id_reserva: UUID, id_biblioteca: UUID) -> Optional[Reserva]:
        """
        Obtiene una reserva específica por su ID.

        Args:
            id_reserva (UUID): Identificador único de la reserva.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            Optional[Reserva]: Objeto de la reserva si existe, None en caso contrario.
        """
        return self.db.query(Reserva).filter(Reserva.id_reserva == id_reserva, Reserva.id_biblioteca == id_biblioteca).first()
    
    def obtener_reservas(self, id_biblioteca: UUID, skip: int = 0, limit: int = 100) -> List[Reserva]:
        """
        Obtiene una lista de reservas de una biblioteca con paginación.

        Args:
            id_biblioteca (UUID): Identificador único de la biblioteca.
            skip (int, opcional): Número de registros a omitir. Por defecto 0.
            limit (int, opcional): Número máximo de registros a retornar. Por defecto 100.

        Returns:
            List[Reserva]: Lista de reservas encontradas.
        """
        return (self.db.query(Reserva).options(joinedload(Reserva.cliente),joinedload(Reserva.material)).filter(Reserva.id_biblioteca == id_biblioteca).offset(skip).limit(limit).all())
        
    def obtener_reservas_por_cliente(self, cod_cliente: UUID, id_biblioteca: UUID) -> List[Reserva]:
        """
        Obtiene todas las reservas realizadas por un cliente en una biblioteca.

        Args:
            cod_cliente (UUID): Identificador único del cliente.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            List[Reserva]: Lista de reservas asociadas al cliente.
        """
        return self.db.query(Reserva).filter(Reserva.cod_cliente == cod_cliente, Reserva.id_biblioteca == id_biblioteca).all()

    def obtener_reservas_por_fecha(self, fecha_reserva: date, id_biblioteca: UUID) -> List[Reserva]:
        """
        Obtiene todas las reservas realizadas en una fecha específica.

        Args:
            fecha_reserva (date): Fecha de la reserva.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            List[Reserva]: Lista de reservas en la fecha indicada.
        """
        return self.db.query(Reserva).filter(Reserva.fecha_reserva == fecha_reserva, Reserva.id_biblioteca == id_biblioteca).all()
    
    def obtener_reserva_por_material(self, id_material: UUID, id_biblioteca: UUID) -> Optional[Reserva]:
        """
        Obtiene una reserva asociada a un material específico.

        Args:
            id_material (UUID): Identificador único del material.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            Optional[Reserva]: Reserva asociada al material o None si no existe.
        """
        return self.db.query(Reserva).filter(Reserva.id_material == id_material, Reserva.id_biblioteca == id_biblioteca).first()

    def obtener_reservas_por_estado(self, estado: str, id_biblioteca: UUID) -> List[Reserva]:
        """
        Obtiene todas las reservas con un estado específico.

        Args:
            estado (str): Estado de la reserva (ejemplo: "pendiente", "activa", "cancelada").
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            List[Reserva]: Lista de reservas en el estado indicado.
        """
        return self.db.query(Reserva).filter(Reserva.estado == estado, Reserva.id_biblioteca == id_biblioteca).all()

    def actualizar_reserva(self, id_reserva: UUID, id_biblioteca: UUID, id_usuario_edita: UUID = None, **kwargs) -> Optional[Reserva]:
        """
        Actualiza los datos de una reserva existente.

        Args:
            id_reserva (UUID): Identificador único de la reserva.
            id_biblioteca (UUID): Identificador único de la biblioteca.
            id_usuario_edita (UUID, opcional): Identificador del usuario que edita la reserva.
            **kwargs: Campos de la reserva a actualizar (ejemplo: fecha_reserva, estado, id_material, cod_cliente).

        Returns:
            Optional[Reserva]: Reserva actualizada o None si no existe.
        """
        reserva = self.obtener_reserva(id_reserva, id_biblioteca)
        if not reserva:
            return None

        if "fecha_reserva" in kwargs and kwargs["fecha_reserva"] is not None:
            if not isinstance(kwargs["fecha_reserva"], date):
                raise ValueError("La fecha de la reserva debe ser un objeto date")
        
        if "estado" in kwargs and kwargs["estado"] is not None:
            estado = kwargs["estado"].strip()
            if not estado:
                raise ValueError("El estado es obligatorio")
            if len(estado) > 50:
                raise ValueError("El estado no puede exceder 50 caracteres")
            kwargs["estado"] = estado.lower()
        
        if "cod_cliente" in kwargs and kwargs["cod_cliente"] is not None:
            kwargs["cod_cliente"] = kwargs["cod_cliente"]

        if "id_material" in kwargs and kwargs["id_material"] is not None:
            kwargs["id_material"] = kwargs["id_material"]

        if id_usuario_edita is None:
            from entities.Usuario import Usuario
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError("No se encontró un usuario administrador para editar la reserva")
            id_usuario_edita = admin.id_usuario

        reserva.id_usuario_edita = id_usuario_edita

        for key, value in kwargs.items():
            if hasattr(reserva, key):
                setattr(reserva, key, value)

        self.db.commit()
        self.db.refresh(reserva)
        return reserva

    def actualizar_estado(self, id_reserva: UUID, id_biblioteca: UUID, nuevo_estado: str) -> Optional[Reserva]:
        """
        Actualiza el estado de una reserva.

        Args:
            id_reserva (UUID): Identificador único de la reserva.
            id_biblioteca (UUID): Identificador único de la biblioteca.
            nuevo_estado (str): Nuevo estado de la reserva.

        Returns:
            Optional[Reserva]: Reserva actualizada o None si no existe.
        """
        if not nuevo_estado or len(nuevo_estado.strip()) == 0:
            raise ValueError("El estado de la reserva es obligatorio")
        if len(nuevo_estado) > 50:
            raise ValueError("El estado no puede exceder 50 caracteres")
        
        return self.actualizar_reserva(id_reserva, id_biblioteca=id_biblioteca, estado=nuevo_estado.strip().lower())

    def eliminar_reserva(self, id_reserva: UUID, id_biblioteca: UUID) -> bool:
        """
        Elimina una reserva de la base de datos.

        Args:
            id_reserva (UUID): Identificador único de la reserva.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            bool: True si la reserva fue eliminada, False si no se encontró.
        """
        reserva = self.obtener_reserva(id_reserva, id_biblioteca)
        if reserva:
            self.db.delete(reserva)
            self.db.commit()
            return True
        return False