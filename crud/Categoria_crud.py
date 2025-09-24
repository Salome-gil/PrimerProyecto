from typing import List, Optional
from uuid import UUID
from entities.Categoria import Categoria
from sqlalchemy.orm import Session


class CategoriaCRUD:
    """
    Clase para gestionar operaciones CRUD de la entidad Categoria en la base de datos.
    """

    def __init__(self, db: Session):
        """
        Inicializa el CRUD con una sesión de base de datos.

        :param db: Sesión de SQLAlchemy para interactuar con la base de datos.
        :type db: Session
        """
        self.db = db

    def crear_categoria(self, id_biblioteca: UUID, nombre: str, descripcion: str, id_usuario_crea: UUID = None) -> Categoria:
        """
        Crea una nueva categoría en una biblioteca.

        Args:
            id_biblioteca (UUID): Identificador único de la biblioteca.
            nombre (str): Nombre de la categoría.
            descripcion (str): Descripción de la categoría.
            id_usuario_crea (UUID, opcional): Usuario que crea la categoría. 
                Si no se especifica, se asigna un administrador por defecto.

        Returns:
            Categoria: Objeto de la categoría creada.

        Raises:
            ValueError: Si el nombre o la descripción no cumplen las validaciones.
        """

        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre de la categoría es obligatorio")
        if len(nombre) > 150:
            raise ValueError("El nombre no puede exceder 150 caracteres")

        if descripcion and len(descripcion) > 250:
            raise ValueError("La descripción no puede exceder 250 caracteres")
    
        if id_usuario_crea is None:
            from entities.Usuario import Usuario
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError("No se encontró un usuario administrador para crear la categoría")
            id_usuario_crea = admin.id_usuario

        categoria = Categoria(
            id_biblioteca=id_biblioteca,
            nombre=nombre.strip(),
            descripcion=descripcion.strip(),
            id_usuario_crea=id_usuario_crea,
        )

        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def obtener_categoria(self, id_categoria: UUID, id_biblioteca: UUID,) -> Optional[Categoria]:
        """
        Obtiene una categoría específica por su ID y biblioteca.

        Args:
            id_categoria (UUID): Identificador único de la categoría.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            Optional[Categoria]: Categoría encontrada o None si no existe.
        """
        return(self.db.query(Categoria).filter(Categoria.id_categoria == id_categoria, Categoria.id_biblioteca == id_biblioteca).first())

    def obtener_categorias(self, id_biblioteca: UUID, skip: int = 0, limit: int = 100) -> List[Categoria]:
        """
        Obtiene un listado de categorías de una biblioteca con paginación.

        Args:
            id_biblioteca (UUID): Identificador único de la biblioteca.
            skip (int, opcional): Número de registros a omitir. Por defecto 0.
            limit (int, opcional): Número máximo de registros a retornar. Por defecto 100.

        Returns:
            List[Categoria]: Lista de categorías encontradas.
        """
        return self.db.query(Categoria).filter(Categoria.id_biblioteca == id_biblioteca).offset(skip).limit(limit).all()

    def obtener_categoria_por_nombre(self, nombre: str, id_biblioteca: UUID) -> Optional[Categoria]:
        """
        Busca una categoría por su nombre en una biblioteca.

        Args:
            nombre (str): Nombre de la categoría.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            Optional[Categoria]: Categoría encontrada o None si no existe.
        """
        return self.db.query(Categoria).filter(Categoria.nombre == nombre, Categoria.id_biblioteca == id_biblioteca).first()

    def actualizar_categoria(self, id_categoria: UUID, id_biblioteca: UUID, id_usuario_edita: UUID = None, **kwargs) -> Optional[Categoria]:
        """
        Actualiza los datos de una categoría existente.

        Args:
            id_categoria (UUID): Identificador único de la categoría.
            id_biblioteca (UUID): Identificador único de la biblioteca.
            id_usuario_edita (UUID, opcional): Usuario que edita la categoría. 
                Si no se especifica, se asigna un administrador por defecto.
            **kwargs: Campos a actualizar (ej. nombre, descripcion).

        Returns:
            Optional[Categoria]: Categoría actualizada o None si no existe.

        Raises:
            ValueError: Si los valores enviados son inválidos.
        """
        categoria = self.obtener_categoria(id_categoria, id_biblioteca)
        if not categoria:
            return None
        
        if id_usuario_edita is None:
            from entities.Usuario import Usuario
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError("No se encontró un usuario administrador para editar la categoría")
            id_usuario_edita = admin.id_usuario

        categoria.id_usuario_edita = id_usuario_edita

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre de la categoría es obligatorio")
            if len(nombre) > 150:
                raise ValueError("El nombre no puede exceder 150 caracteres")
            kwargs["nombre"] = nombre.strip()

        if "descripcion" in kwargs and kwargs["descripcion"] is not None:
            descripcion = kwargs["descripcion"]
            if len(descripcion.strip()) > 250:
                raise ValueError("La descripción no puede exceder 250 caracteres")
            kwargs["descripcion"] = descripcion.strip()

        for key, value in kwargs.items():
            if hasattr(categoria, key):
                setattr(categoria, key, value)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def eliminar_categoria(self, id_categoria: UUID, id_biblioteca: UUID) -> bool:
        """
        Elimina una categoría por su ID y biblioteca.

        Args:
            id_categoria (UUID): Identificador único de la categoría.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            bool: True si la categoría fue eliminada, False si no existe.
        """
        categoria = self.obtener_categoria(id_categoria, id_biblioteca)
        if categoria:
            self.db.delete(categoria)
            self.db.commit()
            return True
        return False