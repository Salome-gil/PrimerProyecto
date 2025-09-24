import re
from typing import List, Optional, Tuple
from uuid import UUID

from auth.security import PasswordManager
from entities.Usuario import Usuario
from sqlalchemy.orm import Session


class UsuarioCRUD:
    """
    Clase para manejar las operaciones CRUD (Crear, Leer, Actualizar y Eliminar) 
    relacionadas con la entidad `Usuario` en la base de datos.
    """

    def __init__(self, db: Session):
        """
        Inicializa el CRUD de Usuario con la sesión de base de datos.

        Args:
            db (Session): Sesión activa de SQLAlchemy.
        """
        self.db = db

    def _validar_email(self, email: str) -> bool:
        """
        Valida el formato de un correo electrónico.

        Args:
            email (str): Dirección de correo a validar.

        Returns:
            bool: True si el formato es válido, False en caso contrario.
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def _validar_telefono(self, telefono: str) -> bool:
        """
        Valida el formato de un número de teléfono.

        Args:
            telefono (str): Número de teléfono a validar.

        Returns:
            bool: True si el formato es válido, False en caso contrario.
        """
        pattern = r"^\+?[\d\s\-\(\)]{7,15}$"
        return re.match(pattern, telefono) is not None

    def _validar_nombre_usuario(self, nombre_usuario: str) -> bool:
        """
        Valida el formato de un nombre de usuario.

        Args:
            nombre_usuario (str): Nombre de usuario a validar.

        Returns:
            bool: True si el formato es válido, False en caso contrario.
        """
        pattern = r"^[a-zA-Z0-9_]{3,20}$"
        return re.match(pattern, nombre_usuario) is not None

    def crear_usuario(self, nombre: str, nombre_usuario: str, email: str, contraseña: str, telefono: str = None, es_admin: bool = False,) -> Usuario:
        """
        Crea un nuevo usuario en la base de datos.

        Args:
            nombre (str): Nombre completo del usuario.
            nombre_usuario (str): Nombre de usuario único.
            email (str): Correo electrónico único del usuario.
            contraseña (str): Contraseña en texto plano.
            telefono (str, optional): Número de teléfono. Default None.
            es_admin (bool, optional): Indica si el usuario es administrador. Default False.

        Returns:
            Usuario: Usuario creado.

        Raises:
            ValueError: Si los datos son inválidos o ya existen en la base de datos.
        """

        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre es obligatorio")

        if len(nombre) > 100:
            raise ValueError("El nombre no puede exceder 100 caracteres")

        if not nombre_usuario or not self._validar_nombre_usuario(nombre_usuario):
            raise ValueError(
                "El nombre de usuario debe tener entre 3-20 caracteres y solo contener letras, números y guiones bajos"
            )

        if self.obtener_usuario_por_nombre_usuario(nombre_usuario):
            raise ValueError("El nombre de usuario ya está registrado")

        if not email or not self._validar_email(email):
            raise ValueError("Email inválido")

        if self.obtener_usuario_por_email(email):
            raise ValueError("El email ya está registrado")

        if not contraseña:
            raise ValueError("La contraseña es obligatoria")

        es_valida, mensaje = PasswordManager.validate_password_strength(contraseña)
        if not es_valida:
            raise ValueError(f"Contraseña inválida: {mensaje}")

        if telefono and not self._validar_telefono(telefono):
            raise ValueError("Formato de teléfono inválido")

        contraseña_hash = PasswordManager.hash_password(contraseña)

        usuario = Usuario(
            nombre=nombre.strip(),
            nombre_usuario=nombre_usuario.strip().lower(),
            email=email.lower().strip(),
            contraseña_hash=contraseña_hash,
            telefono=telefono.strip() if telefono else None,
            es_admin=es_admin,
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def obtener_usuario(self, usuario_id: UUID) -> Optional[Usuario]:
        """
        Obtener un usuario por ID

        Args:
            usuario_id: UUID del usuario

        Returns:
            Usuario encontrado o None
        """
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def obtener_usuario_por_email(self, email: str) -> Optional[Usuario]:
        """
        Obtener un usuario por email

        Args:
            email: Email del usuario

        Returns:
            Usuario encontrado o None
        """
        return (
            self.db.query(Usuario)
            .filter(Usuario.email == email.lower().strip())
            .first()
        )

    def obtener_usuario_por_nombre_usuario(
        self, nombre_usuario: str
    ) -> Optional[Usuario]:
        """
        Obtener un usuario por nombre de usuario

        Args:
            nombre_usuario: Nombre de usuario

        Returns:
            Usuario encontrado o None
        """
        return (
            self.db.query(Usuario)
            .filter(Usuario.nombre_usuario == nombre_usuario.lower().strip())
            .first()
        )

    def autenticar_usuario(
        self, nombre_usuario: str, contraseña: str
    ) -> Optional[Usuario]:
        """
        Autenticar un usuario con nombre de usuario y contraseña

        Args:
            nombre_usuario: Nombre de usuario o email
            contraseña: Contraseña en texto plano

        Returns:
            Usuario autenticado o None si las credenciales son inválidas
        """
        # Buscar por nombre de usuario o email
        usuario = self.obtener_usuario_por_nombre_usuario(nombre_usuario)
        if not usuario:
            usuario = self.obtener_usuario_por_email(nombre_usuario)

        if not usuario or not usuario.activo:
            return None

        if PasswordManager.verify_password(contraseña, usuario.contraseña_hash):
            return usuario

        return None

    def cambiar_contraseña(
        self, usuario_id: UUID, contraseña_actual: str, nueva_contraseña: str
    ) -> bool:
        """
        Cambiar la contraseña de un usuario

        Args:
            usuario_id: UUID del usuario
            contraseña_actual: Contraseña actual
            nueva_contraseña: Nueva contraseña

        Returns:
            True si se cambió exitosamente, False en caso contrario

        Raises:
            ValueError: Si la contraseña actual es incorrecta o la nueva es inválida
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return False

        if not PasswordManager.verify_password(
            contraseña_actual, usuario.contraseña_hash
        ):
            raise ValueError("La contraseña actual es incorrecta")

        es_valida, mensaje = PasswordManager.validate_password_strength(
            nueva_contraseña
        )
        if not es_valida:
            raise ValueError(f"Nueva contraseña inválida: {mensaje}")

        usuario.contraseña_hash = PasswordManager.hash_password(nueva_contraseña)
        self.db.commit()
        return True

    def obtener_usuarios(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """
        Obtener lista de usuarios con paginación

        Args:
            skip: Número de registros a omitir
            limit: Límite de registros a retornar

        Returns:
            Lista de usuarios
        """
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    def actualizar_usuario(self, usuario_id: UUID, **kwargs) -> Optional[Usuario]:
        """
        Actualizar un usuario con validaciones

        Args:
            usuario_id: UUID del usuario
            **kwargs: Campos a actualizar

        Returns:
            Usuario actualizado o None

        Raises:
            ValueError: Si los datos no son válidos
        """
        usuario = self.obtener_usuario(usuario_id)
        if not usuario:
            return None

        if "email" in kwargs:
            email = kwargs["email"]
            if not self._validar_email(email):
                raise ValueError("Email inválido")
            if (
                self.obtener_usuario_por_email(email)
                and self.obtener_usuario_por_email(email).id != usuario_id
            ):
                raise ValueError("El email ya está registrado")
            kwargs["email"] = email.lower().strip()

        if "telefono" in kwargs and kwargs["telefono"]:
            if not self._validar_telefono(kwargs["telefono"]):
                raise ValueError("Formato de teléfono inválido")
            kwargs["telefono"] = kwargs["telefono"].strip()

        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre es obligatorio")
            if len(nombre) > 100:
                raise ValueError("El nombre no puede exceder 100 caracteres")
            kwargs["nombre"] = nombre.strip()

        if "nombre_usuario" in kwargs:
            nombre_usuario = kwargs["nombre_usuario"]
            if not nombre_usuario or not self._validar_nombre_usuario(nombre_usuario):
                raise ValueError(
                    "El nombre de usuario debe tener entre 3-20 caracteres y solo contener letras, números y guiones bajos"
                )
            if (
                self.obtener_usuario_por_nombre_usuario(nombre_usuario)
                and self.obtener_usuario_por_nombre_usuario(nombre_usuario).id
                != usuario_id
            ):
                raise ValueError("El nombre de usuario ya está registrado")
            kwargs["nombre_usuario"] = nombre_usuario.strip().lower()

        if "contraseña" in kwargs:
            contraseña = kwargs["contraseña"]
            es_valida, mensaje = PasswordManager.validate_password_strength(contraseña)
            if not es_valida:
                raise ValueError(f"Contraseña inválida: {mensaje}")
            kwargs["contraseña_hash"] = PasswordManager.hash_password(contraseña)
            del kwargs["contraseña"]  # Eliminar la contraseña en texto plano

        for key, value in kwargs.items():
            if hasattr(usuario, key):
                setattr(usuario, key, value)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def eliminar_usuario(self, usuario_id: UUID) -> bool:
        """
        Eliminar un usuario

        Args:
            usuario_id: UUID del usuario

        Returns:
            True si se eliminó, False si no existe
        """
        usuario = self.obtener_usuario(usuario_id)
        if usuario:
            self.db.delete(usuario)
            self.db.commit()
            return True
        return False

    def desactivar_usuario(self, usuario_id: UUID) -> Optional[Usuario]:
        """
        Desactivar un usuario (soft delete)

        Args:
            usuario_id: UUID del usuario

        Returns:
            Usuario desactivado o None
        """
        return self.actualizar_usuario(usuario_id, activo=False)

    def obtener_usuarios_admin(self) -> List[Usuario]:
        """
        Obtener todos los usuarios administradores

        Returns:
            Lista de usuarios administradores
        """
        return self.db.query(Usuario).filter(Usuario.es_admin == True).all()

    def es_admin(self, usuario_id: UUID) -> bool:
        """
        Verificar si un usuario es administrador

        Args:
            usuario_id: UUID del usuario

        Returns:
            True si es administrador, False en caso contrario
        """
        usuario = self.obtener_usuario(usuario_id)
        return usuario.es_admin if usuario else False

    def obtener_admin_por_defecto(self) -> Optional[Usuario]:
        """
        Obtener el usuario administrador por defecto

        Returns:
            Usuario administrador por defecto o None
        """
        return (
            self.db.query(Usuario)
            .filter(Usuario.email == "admin@system.com", Usuario.es_admin == True)
            .first()
        )