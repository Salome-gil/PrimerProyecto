"""ENTIDAD USUARIO DE LA CLASE USUARIO"""
import uuid
from sqlalchemy.dialects.postgresql import UUID
from database.config import Base
from sqlalchemy import Boolean, Column, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

"""ATRIBUTOS DE LA ENTIDAD:
    id_usuario: uuid, clave primaria
    nombre: Nombre completo del usuario.
    nombre_usuario: Nombre de usuario único para inicio de sesión.
    email: Correo electrónico único del usuario.
    contraseña_hash: Contraseña almacenada en formato hash.
    telefono: Número de teléfono del usuario (opcional).
    activo: Indica si la cuenta está activa (por defecto True).
    es_admin: Define si el usuario tiene privilegios de administrador."""

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre = Column(String(100), nullable=False)
    nombre_usuario = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    contraseña_hash = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=True)
    activo = Column(Boolean, default=True)
    es_admin = Column(Boolean, default=False)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Usuario(id_usuario={self.id_usuario}, nombre='{self.nombre}')>"