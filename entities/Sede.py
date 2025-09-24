"""ENTIDAD SEDE DE LA CLASE SEDE"""
import uuid
from sqlalchemy.dialects.postgresql import UUID
from database.config import Base
from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

"""ATRIBUTOS DE LA ENTIDAD
    id_sede: uuid, clave primaria
    nombre: nombre de la sede
    direcion: direccion de la sede"""

class Sede(Base):
    __tablename__ = "sedes"

    id_sede= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre= Column(String(80), nullable=True, unique=True)
    direccion= Column(String(150), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    biblioteca = relationship("Biblioteca", back_populates="sede", uselist=False)
    materiales = relationship("Material_Bibliografico", back_populates="sede")

    #id_usuario_crea = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario", name="fk_sedes_usuario_crea"), nullable=True)
    #id_usuario_edita = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario", name="fk_sedes_usuario_edita"), nullable=True)

    id_usuario_crea = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario", name="fk_sedes_usuario_crea", use_alter=True, deferrable=True), nullable=True)
    id_usuario_edita = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario", name="fk_sedes_usuario_edita", use_alter=True, deferrable=True), nullable=True)

    usuario_crea= relationship("Usuario", foreign_keys=[id_usuario_crea], overlaps="usuario_edita")
    usuario_edita= relationship("Usuario", foreign_keys=[id_usuario_edita], overlaps="usuario_crea")

    def __repr__(self):
        return f"<Sede(id_sede={self.id_sede}, nombre='{self.nombre}', direccion='{self.direccion}')>"