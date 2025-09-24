"""IDENTIDAD CATEGORIA DE LA CLASE CATEGORIA"""
import uuid
from sqlalchemy.dialects.postgresql import UUID
from database.config import Base
from sqlalchemy import Column, ForeignKey, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

"""ATRIBUTOS DE LA ENTIDAD
    id_categoria: uuid, clave primaria
    id_biblioteca: clave foranea de la entidad biblioteca
    nombre: nombre de la categoria
    descripcion: una descripcion breve de la categoria"""

class Categoria(Base):
    __tablename__ = "categorias"

    id_categoria= Column(UUID(as_uuid=True), primary_key= True, default=uuid.uuid4, index=True)
    id_biblioteca = Column(UUID(as_uuid=True), ForeignKey("bibliotecas.id_biblioteca"), nullable=True)
    nombre= Column(String(100), nullable=False, unique= True)
    descripcion= Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    id_usuario_crea = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True)
    id_usuario_edita = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True)

    materiales= relationship("Material_Bibliografico", back_populates="categoria")
    biblioteca = relationship("Biblioteca")
    
    usuario_crea= relationship("Usuario", foreign_keys=[id_usuario_crea], overlaps="usuario_edita")
    usuario_edita= relationship("Usuario", foreign_keys=[id_usuario_edita], overlaps="usuario_crea")

    def __repr__(self):
        return f"<Categoria(id_categoria={self.id_categoria}, nombre='{self.nombre}', descripcion='{self.descripcion}')>"
