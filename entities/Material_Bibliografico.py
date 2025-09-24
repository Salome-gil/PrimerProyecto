"""ENTIDAD MATERIAL_BIBLIOGRAFICOS DE LA CLASE MATERIAL_BIBLIOGRAFICO"""
import uuid
from sqlalchemy.dialects.postgresql import UUID
from database.config import Base
from sqlalchemy import Column, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

"""ATRIBUTOS DE LA ENTIDAD:
    id_material: uuid, clave primaria
    id_biblioteca: clave foranea de la entidad biblioteca
    titulo: titulo del material bibliografico
    autor:autor o autores del materia bibliografico
    estado: si se encuentra prestado, reservado o disponible"""

class Material_Bibliografico(Base):
    __tablename__ = "materiales"

    id_material= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id_biblioteca = Column(UUID(as_uuid=True), ForeignKey("bibliotecas.id_biblioteca"), nullable=True)
    titulo= Column(String(80), nullable=True)
    autor= Column(String(80), nullable=True)
    estado= Column(String(80), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    
    id_categoria = Column(UUID(as_uuid=True), ForeignKey("categorias.id_categoria"))
    id_sede = Column(UUID(as_uuid=True), ForeignKey("sedes.id_sede"))

    id_usuario_crea = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True)
    id_usuario_edita = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True)

    sede = relationship("Sede", back_populates="materiales")
    categoria = relationship("Categoria", back_populates="materiales")
    prestamos = relationship("Prestamo", back_populates="material")
    reservas = relationship("Reserva", back_populates="material")
    biblioteca = relationship("Biblioteca")

    usuario_crea= relationship("Usuario", foreign_keys=[id_usuario_crea], overlaps="usuario_edita")
    usuario_edita= relationship("Usuario", foreign_keys=[id_usuario_edita], overlaps="usuario_crea")

    def __repr__(self):
        return f"<Material_Bibliografico(id_material={self.id_material}, titulo='{self.titulo}', autor='{self.autor}', estado='{self.estado}')>"