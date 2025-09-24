from typing import List, Optional
from uuid import UUID
from entities.Sede import Sede
from sqlalchemy.orm import Session
from sqlalchemy import func


class SedeCRUD:
    """
    Clase para manejar las operaciones CRUD (Crear, Leer, Actualizar y Eliminar) 
    relacionadas con la entidad `Sede` en la base de datos.
    """

    def __init__(self, db: Session):
        """
        Inicializa el CRUD de Sede con la sesión de base de datos.

        Args:
            db (Session): Sesión activa de SQLAlchemy.
        """
        self.db = db

    def crear_sede(self, nombre: str, direccion: str, id_usuario_crea: UUID = None) -> Sede:
        """
        Crea una nueva sede en la base de datos.

        Args:
            nombre (str): Nombre de la sede (máx. 150 caracteres).
            direccion (str): Dirección de la sede (máx. 250 caracteres).
            id_usuario_crea (UUID, optional): Identificador del usuario creador.
                Si no se envía, se asigna automáticamente el primer usuario administrador.

        Returns:
            Sede: Objeto `Sede` creado.
        """
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre de la sede es obligatorio")
        if len(nombre) > 80:
            raise ValueError("El nombre no puede exceder 150 caracteres")

        if not direccion or len(direccion.strip()) == 0:
            raise ValueError("La dirección de la sede es obligatoria")
        if len(direccion) > 150:
            raise ValueError("La dirección no puede exceder 250 caracteres")

        if id_usuario_crea is None:
            from entities.Usuario import Usuario
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para crear la sede")
            id_usuario_crea = admin.id_usuario

        sede = Sede(
            nombre= nombre.strip(),
            direccion= direccion.strip(),
            id_usuario_crea= id_usuario_crea,
        )

        self.db.add(sede)
        self.db.commit()
        self.db.refresh(sede)
        return sede

    def obtener_sede(self, id_sede: UUID) -> Optional[Sede]:
        """
        Obtiene una sede por su identificador único.

        Args:
            id_sede (UUID): Identificador único de la sede.

        Returns:
            Optional[Sede]: Objeto `Sede` si existe, o None en caso contrario.
        """
        return self.db.query(Sede).filter(Sede.id_sede == id_sede).first()

    def obtener_sedes(self, skip: int = 0, limit: int = 100) -> List[Sede]:
        """
        Obtiene una lista de sedes con paginación.

        Args:
            skip (int, optional): Número de registros a omitir. Default 0.
            limit (int, optional): Número máximo de registros a devolver. Default 100.

        Returns:
            List[Sede]: Lista de sedes.
        """
        return self.db.query(Sede).offset(skip).limit(limit).all()

    def obtener_sede_por_nombre(self, nombre: str) -> Optional[Sede]:
        """
        Busca una sede por su nombre (sin distinguir mayúsculas/minúsculas).

        Args:
            nombre (str): Nombre de la sede.

        Returns:
            Optional[Sede]: Objeto `Sede` si existe, o None en caso contrario.
        """
        nombre = nombre.strip()
        return (self.db.query(Sede).filter(func.lower(Sede.nombre) == nombre.lower()).first())

    def actualizar_sede(self, id_sede: UUID, id_usuario_edita: UUID = None, **kwargs) -> Optional[Sede]:
        """
        Actualiza los datos de una sede existente.

        Args:
            id_sede (UUID): Identificador único de la sede.
            id_usuario_edita (UUID, optional): Identificador del usuario que edita.
                Si no se envía, se asigna automáticamente el primer usuario administrador.
            **kwargs: Campos a actualizar (ej. nombre, direccion).

        Returns:
            Optional[Sede]: Sede actualizada o None si no existe.
        """
        sede = self.obtener_sede(id_sede)
        if not sede:
            return None

        if id_usuario_edita is None:
            from entities.Usuario import Usuario
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError("No se encontró un usuario administrador para editar la sede")
            id_usuario_edita = admin.id_usuario

        sede.id_usuario_edita = id_usuario_edita

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre de la sede es obligatorio")
            if len(nombre) > 150:
                raise ValueError("El nombre no puede exceder 150 caracteres")
            kwargs["nombre"] = nombre.strip()

        if "direccion" in kwargs:
            direccion = kwargs["direccion"]
            if not direccion or len(direccion.strip()) == 0:
                raise ValueError("La dirección de la sede es obligatoria")
            if len(direccion) > 250:
                raise ValueError("La dirección no puede exceder 250 caracteres")
            kwargs["direccion"] = direccion.strip()

        for key, value in kwargs.items():
            if hasattr(sede, key):
                setattr(sede, key, value)
        self.db.commit()
        self.db.refresh(sede)
        return sede

    def eliminar_sede(self, id_sede: UUID) -> bool:
        """
        Elimina una sede de la base de datos.

        Args:
            id_sede (UUID): Identificador único de la sede.

        Returns:
            bool: True si la sede fue eliminada, False si no existe.
        """
        sede = self.obtener_sede(id_sede)
        if sede:
            self.db.delete(sede)
            self.db.commit()
            return True
        return False