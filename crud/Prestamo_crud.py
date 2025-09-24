from datetime import date
from uuid import UUID
from typing import List, Optional
from entities.Prestamo import Prestamo
from sqlalchemy.orm import Session, joinedload


class PrestamoCRUD:
    """
    Clase para realizar operaciones CRUD sobre préstamos en la base de datos.
    """

    def __init__(self, db: Session):
        """
        Inicializa el CRUD con una sesión de base de datos.

        Args:
            db (Session): Sesión de SQLAlchemy para interactuar con la base de datos.
        """
        self.db = db

    def crear_prestamo(self, fecha_prestamo: date, fecha_entrega: date, id_material: UUID, cod_cliente: UUID, id_biblioteca: UUID, id_usuario_crea: UUID = None) -> Prestamo:
        """
        Crea un nuevo préstamo de material bibliográfico.

        Args:
            fecha_prestamo (date): Fecha en la que inicia el préstamo.
            fecha_entrega (date): Fecha en la que debe devolverse el material.
            id_material (UUID): Identificador único del material.
            cod_cliente (UUID): Identificador único del cliente.
            id_biblioteca (UUID): Identificador único de la biblioteca.
            id_usuario_crea (UUID, opcional): Usuario que registra el préstamo.

        Returns:
            Prestamo: Objeto de préstamo creado en la base de datos.
        """
        if not fecha_prestamo:
            raise ValueError("La fecha del préstamo es obligatoria")
        if not fecha_entrega:
            raise ValueError("La fecha de entrega es obligatoria")
        if fecha_entrega < fecha_prestamo:
            raise ValueError("La fecha de entrega no puede ser anterior a la fecha de préstamo")
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
                raise ValueError("No se encontró un usuario administrador para crear el préstamo")
            id_usuario_crea = admin.id_usuario

        prestamo = Prestamo(
            fecha_prestamo=fecha_prestamo,
            fecha_entrega=fecha_entrega,
            id_material=id_material,
            cod_cliente=cod_cliente,
            id_biblioteca=id_biblioteca,
            id_usuario_crea=id_usuario_crea
        )
        
        self.db.add(prestamo)
        self.db.commit()
        self.db.refresh(prestamo)
        return prestamo

    def obtener_prestamo(self, id_prestamo: UUID, id_biblioteca: UUID) -> Optional[Prestamo]:
        """
        Obtiene un préstamo específico.

        Args:
            id_prestamo (UUID): Identificador único del préstamo.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            Optional[Prestamo]: Préstamo encontrado o None si no existe.
        """
        return self.db.query(Prestamo).filter(Prestamo.id == id_prestamo, Prestamo.id_biblioteca == id_biblioteca).first()

    def obtener_prestamos(self, id_biblioteca: UUID, skip: int = 0, limit: int = 100) -> List[Prestamo]:
        """
        Obtiene una lista de préstamos registrados en una biblioteca.

        Args:
            id_biblioteca (UUID): Identificador único de la biblioteca.
            skip (int): Número de registros a omitir.
            limit (int): Número máximo de registros a devolver.

        Returns:
            List[Prestamo]: Lista de préstamos.
        """
        return (self.db.query(Prestamo).options(joinedload(Prestamo.cliente), joinedload(Prestamo.material)).filter(Prestamo.id_biblioteca == id_biblioteca).offset(skip).limit(limit).all())

    def obtener_prestamos_por_fecha_prestamo(self, fecha_prestamo: date, id_biblioteca: UUID) -> List[Prestamo]:
        """
        Obtiene préstamos realizados en una fecha específica.

        Args:
            fecha_prestamo (date): Fecha del préstamo.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            List[Prestamo]: Lista de préstamos realizados en esa fecha.
        """
        return self.db.query(Prestamo).filter(Prestamo.fecha_prestamo == fecha_prestamo, Prestamo.id_biblioteca == id_biblioteca).all()

    def obtener_prestamos_por_fecha_entrega(self, fecha_entrega: date, id_biblioteca: UUID) -> List[Prestamo]:
        """
        Obtiene préstamos cuya fecha de entrega coincide con la indicada.

        Args:
            fecha_entrega (date): Fecha de entrega esperada.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            List[Prestamo]: Lista de préstamos que cumplen con la fecha de entrega.
        """
        return self.db.query(Prestamo).filter(Prestamo.fecha_entrega == fecha_entrega, Prestamo.id_biblioteca == id_biblioteca).all()

    def obtener_prestamo_por_material(self, id_material: UUID, id_biblioteca: UUID) -> Optional[Prestamo]:
        """
        Obtiene el préstamo asociado a un material específico.

        Args:
            id_material (UUID): Identificador único del material.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            Optional[Prestamo]: Préstamo encontrado o None si no existe.
        """
        return self.db.query(Prestamo).filter(Prestamo.id_material == id_material, Prestamo.id_biblioteca == id_biblioteca).first()
    
    def obtener_prestamos_por_cliente(self, cod_cliente: UUID, id_biblioteca: UUID) -> List[Prestamo]:
        """
        Obtiene los préstamos asociados a un cliente específico.

        Args:
            cod_cliente (UUID): Identificador único del cliente.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            List[Prestamo]: Lista de préstamos del cliente.
        """
        return self.db.query(Prestamo).filter(Prestamo.cod_cliente == cod_cliente, Prestamo.id_biblioteca == id_biblioteca).all()

    def actualizar_prestamo(self, id_prestamo: UUID, id_biblioteca: UUID, id_usuario_edita: UUID = None, **kwargs) -> Optional[Prestamo]:
        """
        Actualiza los datos de un préstamo.

        Args:
            id_prestamo (UUID): Identificador único del préstamo.
            id_biblioteca (UUID): Identificador único de la biblioteca.
            id_usuario_edita (UUID, opcional): Usuario que edita el préstamo.
            **kwargs: Campos a actualizar (fecha_prestamo, fecha_entrega, id_material, cod_cliente, etc.).

        Returns:
            Optional[Prestamo]: Préstamo actualizado o None si no existe.
        """
        prestamo = self.obtener_prestamo(id_prestamo, id_biblioteca)
        if not prestamo:
            return None

        if id_usuario_edita is None:
            from entities.Usuario import Usuario
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError("No se encontró un usuario administrador para editar el préstamo")
            id_usuario_edita = admin.id_usuario

        prestamo.id_usuario_edita = id_usuario_edita

        if "fecha_prestamo" in kwargs and kwargs["fecha_prestamo"] is not None:
            fecha_prestamo = kwargs["fecha_prestamo"]
            if not isinstance(fecha_prestamo, date):
                raise ValueError("La fecha de préstamo debe ser un objeto date")
            prestamo.fecha_prestamo = fecha_prestamo

        if "fecha_entrega" in kwargs and kwargs["fecha_entrega"] is not None:
            fecha_entrega = kwargs["fecha_entrega"]
            if not isinstance(fecha_entrega, date):
                raise ValueError("La fecha de entrega debe ser un objeto date")
            prestamo.fecha_entrega = fecha_entrega

        if "id_material" in kwargs and kwargs["id_material"] is not None:
            prestamo.id_material = kwargs["id_material"]

        if "cod_cliente" in kwargs and kwargs["cod_cliente"] is not None:
            prestamo.cod_cliente = kwargs["cod_cliente"]

        for key, value in kwargs.items():
            if hasattr(prestamo, key):
                setattr(prestamo, key, value)

        self.db.commit()
        self.db.refresh(prestamo)
        return prestamo

    def actualizar_fecha_entrega(self, id_prestamo: UUID, id_biblioteca: UUID, nueva_fecha: date, id_usuario_edita: UUID = None) -> Optional[Prestamo]:
        """
        Actualiza únicamente la fecha de entrega de un préstamo.

        Args:
            id_prestamo (UUID): Identificador único del préstamo.
            id_biblioteca (UUID): Identificador único de la biblioteca.
            nueva_fecha (date): Nueva fecha de entrega.
            id_usuario_edita (UUID, opcional): Usuario que edita el préstamo.

        Returns:
            Optional[Prestamo]: Préstamo actualizado o None si no existe.
        """
        if not isinstance(nueva_fecha, date):
            raise ValueError("La nueva fecha de entrega debe ser un objeto date")
        return self.actualizar_prestamo(id_prestamo, id_biblioteca=id_biblioteca, id_usuario_edita=id_usuario_edita, fecha_entrega=nueva_fecha)

    def eliminar_prestamo(self, id_prestamo: UUID, id_biblioteca: UUID) -> bool:
        """
        Elimina un préstamo de la base de datos.

        Args:
            id_prestamo (UUID): Identificador único del préstamo.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            bool: True si se eliminó correctamente, False si no existe.
        """
        prestamo = self.obtener_prestamo(id_prestamo, id_biblioteca)
        if prestamo:
            self.db.delete(prestamo)
            self.db.commit()
            return True
        return False