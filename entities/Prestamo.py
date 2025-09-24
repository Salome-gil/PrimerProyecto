"""ENTIDAD PRESTAMO DE LA CLASE PRESTAMO"""
import uuid
from sqlalchemy.dialects.postgresql import UUID
from database.config import Base
from sqlalchemy import Column, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

"""ATRIBUTOS DE LA ENTIDAD:
    id: uuid, clave primaria
    id_biblioteca: clave foranea de la entidad biblioteca
    fecha_prestamo: fecha en la que fue creado el prestamo
    fecha_entrega: fecha en la que se establece debe entregar el material"""

class Prestamo(Base):
    __tablename__ = "prestamos"

    id= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id_biblioteca = Column(UUID(as_uuid=True), ForeignKey("bibliotecas.id_biblioteca"), nullable=True)
    fecha_prestamo= Column(Date, nullable=True)
    fecha_entrega= Column(Date, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    
    id_material= Column(UUID(as_uuid=True), ForeignKey("materiales.id_material"))
    cod_cliente= Column(UUID(as_uuid=True), ForeignKey("clientes.codigo"))

    id_usuario_crea = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True)
    id_usuario_edita = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True)

    cliente= relationship("Cliente", back_populates="prestamos", foreign_keys=[cod_cliente])
    material= relationship("Material_Bibliografico", back_populates="prestamos", foreign_keys=[id_material])
    biblioteca = relationship("Biblioteca")

    usuario_crea= relationship("Usuario", foreign_keys=[id_usuario_crea], overlaps="usuario_edita")
    usuario_edita= relationship("Usuario", foreign_keys=[id_usuario_edita], overlaps="usuario_crea")

    def __repr__(self):
        return f"<Prestamo(id={self.id}, fecha_prestamo={self.fecha_prestamo}, fecha_entrega={self.fecha_entrega})>"
