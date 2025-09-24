from typing import List, Optional
from uuid import UUID
from entities.Material_Bibliografico import Material_Bibliografico
from sqlalchemy.orm import Session
from sqlalchemy import func


class MaterialBibliograficoCRUD:
    """
    Clase para realizar operaciones CRUD sobre materiales bibliográficos en la base de datos.
    """

    def __init__(self, db: Session):
        """
        Inicializa el CRUD con una sesión de base de datos.

        :param db: Sesión de SQLAlchemy para interactuar con la base de datos.
        :type db: Session
        """
        self.db = db

    def crear_material(self, id_biblioteca: UUID, titulo: str, autor: str, estado: str, id_sede: UUID, id_categoria: UUID, id_usuario_crea: UUID = None) -> Material_Bibliografico:
        """
        Crea un nuevo material bibliográfico.

        Args:
            id_biblioteca (UUID): Identificador único de la biblioteca.
            titulo (str): Título del material.
            autor (str): Autor del material.
            estado (str): Estado del material (ej. disponible, prestado).
            id_sede (UUID): Identificador de la sede asociada.
            id_categoria (UUID): Identificador de la categoría asociada.
            id_usuario_crea (UUID, opcional): Identificador del usuario que crea el registro.

        Returns:
            Material_Bibliografico: Objeto creado en la base de datos.
        """

        if not titulo or len(titulo.strip()) == 0:
            raise ValueError("El título del material es obligatorio")
        if len(titulo) > 150:
            raise ValueError("El título no puede exceder 150 caracteres")
    
        if autor and len(autor.strip()) > 100:
            raise ValueError("El nombre del autor no puede exceder 100 caracteres")
        
        if estado and len(estado.strip()) > 50:
            raise ValueError("El estado no puede exceder 50 caracteres")

        if id_usuario_crea is None:
            from entities.Usuario import Usuario
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError("No se encontró un usuario administrador para crear el material")
            id_usuario_crea = admin.id_usuario

        material = Material_Bibliografico(
            id_biblioteca=id_biblioteca,
            titulo= titulo.strip(),
            autor= autor.strip(),
            estado= estado.strip(),
            id_sede= id_sede,
            id_categoria= id_categoria,
            id_usuario_crea=id_usuario_crea,
        )

        self.db.add(material)
        self.db.commit()
        self.db.refresh(material)
        return material

    def obtener_material(self, id_material: UUID, id_biblioteca: UUID) -> Optional[Material_Bibliografico]:
        """
        Obtiene un material bibliográfico por su ID.

        Args:
            id_material (UUID): Identificador único del material.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            Optional[Material_Bibliografico]: Material encontrado o None si no existe.
        """
        return (self.db.query(Material_Bibliografico).filter(Material_Bibliografico.id_material == id_material, Material_Bibliografico.id_biblioteca == id_biblioteca).first())

    def obtener_materiales(self, id_biblioteca: UUID, skip: int = 0, limit: int = 100) -> List[Material_Bibliografico]:
        """
        Obtiene una lista de materiales bibliográficos.

        Args:
            id_biblioteca (UUID): Identificador único de la biblioteca.
            skip (int): Número de registros a omitir (para paginación).
            limit (int): Número máximo de registros a devolver.

        Returns:
            List[Material_Bibliografico]: Lista de materiales.
        """
        return self.db.query(Material_Bibliografico).filter(Material_Bibliografico.id_biblioteca == id_biblioteca).offset(skip).limit(limit).all()

    def obtener_materiales_por_titulo(self, titulo: str, id_biblioteca: UUID) -> List[Material_Bibliografico]:
        """
        Obtiene materiales por título.

        Args:
            titulo (str): Título del material.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            List[Material_Bibliografico]: Lista de materiales que coinciden con el título.
        """
        titulo = titulo.strip()
        return (self.db.query(Material_Bibliografico).filter(func.lower(Material_Bibliografico.titulo) == titulo.lower(),Material_Bibliografico.id_biblioteca == id_biblioteca).all())
    
    def obtener_materiales_por_autor(self, autor: str, id_biblioteca: UUID) -> List[Material_Bibliografico]:
        """
        Obtiene materiales por autor.

        Args:
            autor (str): Nombre del autor.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            List[Material_Bibliografico]: Lista de materiales que coinciden con el autor.
        """
        autor = autor.strip()
        return (self.db.query(Material_Bibliografico).filter(func.lower(Material_Bibliografico.autor) == autor.lower(),Material_Bibliografico.id_biblioteca == id_biblioteca).all())

    def obtener_materiales_por_estado(self, estado: str, id_biblioteca: UUID) -> List[Material_Bibliografico]:
        """
        Obtiene materiales por estado.

        Args:
            estado (str): Estado del material (ej. disponible, prestado).
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            List[Material_Bibliografico]: Lista de materiales que coinciden con el estado.
        """
        estado = estado.strip()
        return (self.db.query(Material_Bibliografico).filter(Material_Bibliografico.estado == estado, Material_Bibliografico.id_biblioteca == id_biblioteca).all())
    
    def obtener_materiales_por_categoria(self, id_categoria: UUID, id_biblioteca: UUID) -> List[Material_Bibliografico]:
        """
        Obtiene materiales por categoría.

        Args:
            id_categoria (UUID): Identificador único de la categoría.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            List[Material_Bibliografico]: Lista de materiales de la categoría indicada.
        """
        return (self.db.query(Material_Bibliografico).filter(Material_Bibliografico.id_categoria == id_categoria, Material_Bibliografico.id_biblioteca == id_biblioteca).all())

    def actualizar_material(self, id_material: UUID, id_biblioteca: UUID, id_usuario_edita: UUID = None, **kwargs) -> Optional[Material_Bibliografico]:
        """
        Actualiza los datos de un material bibliográfico.

        Args:
            id_material (UUID): Identificador único del material.
            id_biblioteca (UUID): Identificador único de la biblioteca.
            id_usuario_edita (UUID, opcional): Identificador del usuario que edita el registro.
            **kwargs: Campos a actualizar (titulo, autor, estado, id_categoria, id_sede, etc.).

        Returns:
            Optional[Material_Bibliografico]: Material actualizado o None si no existe.
        """
        material = self.obtener_material(id_material, id_biblioteca)
        if not material:
            return None

        if "titulo" in kwargs and kwargs["titulo"] is not None:
            titulo = kwargs["titulo"].strip()
            if not titulo:
                raise ValueError("El título del material es obligatorio")
            if len(titulo) > 80:
                raise ValueError("El título no puede exceder 80 caracteres")
            kwargs["titulo"] = titulo

        if "autor" in kwargs and kwargs["autor"] is not None:
            autor = kwargs["autor"].strip()
            if not autor:
                raise ValueError("El autor es obligatorio")
            if len(autor) > 80:
                raise ValueError("El autor no puede exceder 80 caracteres")
            kwargs["autor"] = autor

        if "estado" in kwargs and kwargs["estado"] is not None:
            estado = kwargs["estado"].strip()
            if not estado:
                raise ValueError("El estado es obligatorio")
            if len(estado) > 80:
                raise ValueError("El estado no puede exceder 80 caracteres")
            kwargs["estado"] = estado

        if "id_categoria" in kwargs and kwargs["id_categoria"] is not None:
            kwargs["id_categoria"] = kwargs["id_categoria"]

        if "id_sede" in kwargs and kwargs["id_sede"] is not None:
            kwargs["id_sede"] = kwargs["id_sede"]

        if id_usuario_edita is None:
            from entities.Usuario import Usuario
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError("No se encontró un usuario administrador para editar el material")
            id_usuario_edita = admin.id_usuario

        material.id_usuario_edita = id_usuario_edita

        for key, value in kwargs.items():
            if hasattr(material, key):
                setattr(material, key, value)

        self.db.commit()
        self.db.refresh(material)
        return material

    def actualizar_estado(self, id_material: UUID, id_biblioteca: UUID, nuevo_estado: str) -> Optional[Material_Bibliografico]:
        """
        Actualiza únicamente el estado de un material.

        Args:
            id_material (UUID): Identificador único del material.
            id_biblioteca (UUID): Identificador único de la biblioteca.
            nuevo_estado (str): Nuevo estado del material.

        Returns:
            Optional[Material_Bibliografico]: Material actualizado o None si no existe.
        """
        if not nuevo_estado or len(nuevo_estado.strip()) == 0:
            raise ValueError("El estado del material es obligatorio")
        if len(nuevo_estado) > 80:
            raise ValueError("El estado no puede exceder 80 caracteres")
    
        return self.actualizar_material(id_material, id_biblioteca=id_biblioteca, estado= nuevo_estado)

    def eliminar_material(self, id_material: UUID, id_biblioteca: UUID) -> bool:
        """
        Elimina un material de la base de datos.

        Args:
            id_material (UUID): Identificador único del material.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            bool: True si fue eliminado, False si no se encontró.
        """
        material = self.obtener_material(id_material, id_biblioteca)
        if material:
            self.db.delete(material)
            self.db.commit()
            return True
        return False