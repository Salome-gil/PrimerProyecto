from typing import List, Optional
from uuid import UUID
from entities.Biblioteca import Biblioteca
from entities.Sede import Sede
from sqlalchemy.orm import Session
from sqlalchemy import func


class BibliotecaCRUD:
    """
    Clase para gestionar operaciones CRUD de la entidad Biblioteca en la base de datos.
    """

    def __init__(self, db: Session):
        """
        Inicializa el CRUD de Biblioteca.

        Args:
            db (Session): Sesión de la base de datos de SQLAlchemy.
        """
        self.db = db

    def crear_biblioteca(self, nombre: str, id_sede: UUID, id_usuario_crea: UUID = None) -> Biblioteca:
        """
        Crea una nueva biblioteca en la base de datos.

        Args:
            nombre (str): Nombre de la biblioteca.
            id_sede (UUID): Identificador único de la sede asociada.
            id_usuario_crea (UUID, opcional): Usuario que crea la biblioteca. 
                Si no se especifica, se asigna un administrador por defecto.

        Returns:
            Biblioteca: Objeto de la biblioteca creada.

        Raises:
            ValueError: Si el nombre es inválido o la sede no existe.
        """

        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre de la biblioteca es obligatorio")
        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")
        
        sede = self.db.query(Sede).filter(Sede.id_sede == id_sede).first()
        if not sede:
            raise ValueError("La sede especificada no existe")
        
        if id_usuario_crea is None:
            from entities.Usuario import Usuario
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para crear la biblioteca"
                )
            id_usuario_crea = admin.id_usuario


        biblioteca = Biblioteca(
            nombre=nombre.strip(), 
            id_sede=id_sede,
            id_usuario_crea=id_usuario_crea)

        self.db.add(biblioteca)
        self.db.commit()
        self.db.refresh(biblioteca)
        return biblioteca

    def obtener_biblioteca(self, id_biblioteca: UUID) -> Optional[Biblioteca]:
        """
        Obtiene una biblioteca por su ID.

        Args:
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            Optional[Biblioteca]: La biblioteca encontrada o None si no existe.
        """
        return self.db.query(Biblioteca).filter(Biblioteca.id_biblioteca == id_biblioteca).first()

    def obtener_bibliotecas(self, skip: int = 0, limit: int = 100) -> List[Biblioteca]:
        """
        Obtiene un listado de bibliotecas con paginación.

        Args:
            skip (int, opcional): Número de registros a omitir. Por defecto 0.
            limit (int, opcional): Número máximo de registros a retornar. Por defecto 100.

        Returns:
            List[Biblioteca]: Lista de bibliotecas encontradas.
        """
        return self.db.query(Biblioteca).offset(skip).limit(limit).all()

    def obtener_biblioteca_por_nombre(self, nombre: str) -> Optional[Biblioteca]:
        """
        Busca una biblioteca por su nombre.

        Args:
            nombre (str): Nombre de la biblioteca.

        Returns:
            Optional[Biblioteca]: Biblioteca encontrada o None si no existe.
        """
        return (self.db.query(Biblioteca).filter(func.lower(Biblioteca.nombre) == nombre.strip().lower()).first())

    def obtener_biblioteca_por_sede(self, id_sede: UUID):
        """
        Busca una biblioteca por el ID de su sede.

        Args:
            id_sede (UUID): Identificador único de la sede.

        Returns:
            Optional[Biblioteca]: Biblioteca encontrada o None si no existe.
        """
        return self.db.query(Biblioteca).filter_by(id_sede=id_sede).first()

    def actualizar_biblioteca(self, id_biblioteca: UUID, id_usuario_edita: UUID = None, **kwargs) -> Optional[Biblioteca]:
        """
        Actualiza los datos de una biblioteca existente.

        Args:
            id_biblioteca (UUID): Identificador único de la biblioteca.
            id_usuario_edita (UUID, opcional): Usuario que edita la biblioteca. 
                Si no se especifica, se asigna un administrador por defecto.
            **kwargs: Campos a actualizar (ej. nombre, id_sede).

        Returns:
            Optional[Biblioteca]: La biblioteca actualizada o None si no existe.

        Raises:
            ValueError: Si se envían valores inválidos o la sede no existe.
        """
        biblioteca = self.obtener_biblioteca(id_biblioteca)
        if not biblioteca:
            return None
        
        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre de la biblioteca es obligatorio")
            if len(nombre) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")
            kwargs["nombre"] = nombre.strip()

        if "id_sede" in kwargs:
            id_sede = kwargs["id_sede"]
            sede = self.db.query(Sede).filter(Sede.id_sede == id_sede).first()
            if not sede:
                raise ValueError("La sede especificada no existe")
            
        if id_usuario_edita is None:
            from entities.Usuario import Usuario
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError("No se encontró un usuario administrador para editar la biblioteca")
            id_usuario_edita = admin.id_usuario

        biblioteca.id_usuario_edita = id_usuario_edita

        for key, value in kwargs.items():
            if hasattr(biblioteca, key):
                setattr(biblioteca, key, value)
        self.db.commit()
        self.db.refresh(biblioteca)
        return biblioteca

    def eliminar_biblioteca(self, id_biblioteca: UUID) -> bool:
        """
        Elimina una biblioteca por su ID.

        Args:
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            bool: True si la biblioteca fue eliminada, False si no existe.
        """
        biblioteca = self.obtener_biblioteca(id_biblioteca)
        if biblioteca:
            self.db.delete(biblioteca)
            self.db.commit()
            return True
        return False