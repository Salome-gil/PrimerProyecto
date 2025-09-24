from datetime import date
from uuid import UUID
from typing import List, Optional
from entities.Sancion import Sancion
from sqlalchemy.orm import Session


class SancionCRUD:
    """
    Clase para realizar operaciones CRUD sobre sanciones en la base de datos.
    """

    def __init__(self, db: Session):
        """
        Inicializa el CRUD con una sesión de base de datos.

        Args:
            db (Session): Sesión de SQLAlchemy para interactuar con la base de datos.
        """
        self.db = db

    def crear_sancion(self, motivo: str, fecha_sancion: date, monto: float, cod_cliente: UUID, id_biblioteca: UUID, id_usuario_crea: UUID = None) -> Sancion:
        """
        Crea una nueva sanción en la base de datos.

        Args:
            motivo (str): Motivo de la sanción (máx. 150 caracteres).
            fecha_sancion (date): Fecha en la que se aplica la sanción.
            monto (float): Monto de la sanción, debe ser positivo.
            cod_cliente (UUID): Identificador único del cliente sancionado.
            id_biblioteca (UUID): Identificador único de la biblioteca.
            id_usuario_crea (UUID, opcional): Identificador del usuario que crea la sanción. 
                                              Si no se proporciona, se asigna un administrador.

        Returns:
            Sancion: Objeto de la sanción creada.
        """
        if not motivo or len(motivo.strip()) == 0:
            raise ValueError("El motivo de la sanción es obligatorio")
        if len(motivo.strip()) > 150:
            raise ValueError("El motivo no puede exceder 150 caracteres")

        if not fecha_sancion:
            raise ValueError("La fecha de la sanción es obligatoria")

        if monto is None or monto < 0:
            raise ValueError("El monto de la sanción es obligatorio y debe ser positivo")

        if not cod_cliente:
            raise ValueError("El cliente es obligatorio")
        if not id_biblioteca:
            raise ValueError("La biblioteca es obligatoria")

        if id_usuario_crea is None:
            from entities.Usuario import Usuario
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError("No se encontró un usuario administrador para crear la sanción")
            id_usuario_crea = admin.id_usuario

        sancion = Sancion(
            motivo= motivo.strip(),
            fecha_sancion= fecha_sancion,
            monto= monto,
            cod_cliente= cod_cliente,
            id_biblioteca=id_biblioteca,
            id_usuario_crea= id_usuario_crea,
        )

        self.db.add(sancion)
        self.db.commit()
        self.db.refresh(sancion)
        return sancion

    def obtener_sancion(self, id_sancion: UUID, id_biblioteca: UUID) -> Optional[Sancion]:
        """
        Obtiene una sanción específica por su ID.

        Args:
            id_sancion (UUID): Identificador único de la sanción.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            Optional[Sancion]: Objeto de la sanción si existe, None en caso contrario.
        """
        return self.db.query(Sancion).filter(Sancion.id_sancion == id_sancion, Sancion.id_biblioteca == id_biblioteca).first()

    def obtener_sanciones(self, id_biblioteca: UUID, skip: int = 0, limit: int = 100) -> List[Sancion]:
        """
        Obtiene una lista de sanciones de una biblioteca con paginación.

        Args:
            id_biblioteca (UUID): Identificador único de la biblioteca.
            skip (int, opcional): Número de registros a omitir. Por defecto 0.
            limit (int, opcional): Número máximo de registros a retornar. Por defecto 100.

        Returns:
            List[Sancion]: Lista de sanciones encontradas.
        """
        return self.db.query(Sancion).filter(Sancion.id_biblioteca == id_biblioteca).offset(skip).limit(limit).all()

    def obtener_sanciones_por_motivo(self, motivo: str, id_biblioteca: UUID) -> List[Sancion]:
        """
        Obtiene todas las sanciones con un motivo específico.

        Args:
            motivo (str): Motivo de la sanción.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            List[Sancion]: Lista de sanciones con el motivo indicado.
        """
        return self.db.query(Sancion).filter(Sancion.motivo == motivo, Sancion.id_biblioteca == id_biblioteca).all()
    
    def obtener_sanciones_por_fecha_sancion(self, fecha_sancion: date, id_biblioteca: UUID) -> List[Sancion]:
        """
        Obtiene todas las sanciones aplicadas en una fecha específica.

        Args:
            fecha_sancion (date): Fecha de la sanción.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            List[Sancion]: Lista de sanciones en la fecha indicada.
        """
        return self.db.query(Sancion).filter(Sancion.fecha_sancion == fecha_sancion, Sancion.id_biblioteca == id_biblioteca).all()
    
    def obtener_sanciones_por_monto(self, monto: float, id_biblioteca: UUID) -> List[Sancion]:
        """
        Obtiene todas las sanciones con un monto específico.

        Args:
            monto (float): Monto de la sanción.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            List[Sancion]: Lista de sanciones con el monto indicado.
        """
        return self.db.query(Sancion).filter(Sancion.monto == monto, Sancion.id_biblioteca == id_biblioteca).all()
    
    def obtener_sanciones_por_cliente(self, cod_cliente: UUID, id_biblioteca: UUID) -> List[Sancion]:
        """
        Obtiene todas las sanciones aplicadas a un cliente específico.

        Args:
            cod_cliente (UUID): Identificador único del cliente.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            List[Sancion]: Lista de sanciones asociadas al cliente.
        """
        return self.db.query(Sancion).filter(Sancion.cod_cliente == cod_cliente, Sancion.id_biblioteca == id_biblioteca).all()

    def actualizar_sancion(self, id_sancion: UUID, id_biblioteca: UUID, id_usuario_edita: UUID = None, **kwargs) -> Optional[Sancion]:
        """
        Actualiza los datos de una sanción existente.

        Args:
            id_sancion (UUID): Identificador único de la sanción.
            id_biblioteca (UUID): Identificador único de la biblioteca.
            id_usuario_edita (UUID, opcional): Identificador del usuario que edita la sanción.
            **kwargs: Campos de la sanción a actualizar (ejemplo: motivo, fecha_sancion, monto, cod_cliente).

        Returns:
            Optional[Sancion]: Sanción actualizada o None si no existe.
        """
        sancion = self.obtener_sancion(id_sancion, id_biblioteca)
        if not sancion:
            return None

        if "motivo" in kwargs and kwargs["motivo"] is not None:
            motivo = kwargs["motivo"].strip()
            if not motivo:
                raise ValueError("El motivo es obligatorio")
            if len(motivo) > 150:
                raise ValueError("El motivo no puede exceder 150 caracteres")
            kwargs["motivo"] = motivo

        if "fecha_sancion" in kwargs and kwargs["fecha_sancion"] is not None:
            if not isinstance(kwargs["fecha_sancion"], date):
                raise ValueError("La fecha de la sanción debe ser un objeto date")

        if "monto" in kwargs and kwargs["monto"] is not None:
            try:
                kwargs["monto"] = float(kwargs["monto"])
            except ValueError:
                raise ValueError("El monto debe ser un número válido")

        if "cod_cliente" in kwargs and kwargs["cod_cliente"] is not None:
            kwargs["cod_cliente"] = kwargs["cod_cliente"]

        if id_usuario_edita is None:
            from entities.Usuario import Usuario
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError("No se encontró un usuario administrador para editar la sanción")
            id_usuario_edita = admin.id_usuario

        sancion.id_usuario_edita = id_usuario_edita

        for key, value in kwargs.items():
            if hasattr(sancion, key):
                setattr(sancion, key, value)

        self.db.commit()
        self.db.refresh(sancion)
        return sancion
    
    def eliminar_sancion(self, id_sancion: UUID, id_biblioteca: UUID) -> bool:
        """
        Elimina una sanción de la base de datos.

        Args:
            id_sancion (UUID): Identificador único de la sanción.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            bool: True si la sanción fue eliminada, False si no se encontró.
        """
        sancion = self.obtener_sancion(id_sancion, id_biblioteca)
        if sancion:
            self.db.delete(sancion)
            self.db.commit()
            return True
        return False