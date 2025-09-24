"""IDENTIDAD DE LA CLASE BIBLIOTECA"""
import uuid
from sqlalchemy.dialects.postgresql import UUID
from database.config import Base
from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
"""Atributos de la entidad:
    id_biblioteca: UUID,clave primaria
    nombre: nombre de la biblioteca 
    id_sede: id foranea de la entidad sede
    """

class Biblioteca(Base):

    __tablename__ = "bibliotecas"

    id_biblioteca = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    nombre = Column(String(100), unique=True, nullable=False)
    id_sede = Column(UUID(as_uuid=True), ForeignKey("sedes.id_sede"))
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    sede = relationship("Sede", back_populates="biblioteca")
    clientes = relationship("Cliente", back_populates="biblioteca")

    id_usuario_crea = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"))
    id_usuario_edita = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"))

    usuario_crea= relationship("Usuario", foreign_keys=[id_usuario_crea], overlaps="usuario_edita")
    usuario_edita= relationship("Usuario", foreign_keys=[id_usuario_edita], overlaps="usuario_crea")

    def __repr__(self):
        return f"<Biblioteca(id_biblioteca={self.id_biblioteca}, nombre='{self.nombre}')>"