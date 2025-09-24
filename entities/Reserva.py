"""ENTIDAD RESERVA DE LA CLASE RESERVA"""
import uuid
from sqlalchemy.dialects.postgresql import UUID
from database.config import Base
from sqlalchemy import Column, Date, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

"""ATRIBUTOS DE LA ENTIDAD:
    id_reserva: uuid, clave primaria
    id_biblioteca: clave foranea de la entidad biblioteca
    fecha_reserva: fecha en la que se hizo la reserva
    estado: si la reserva esta activa o no"""

class Reserva(Base):
    __tablename__ = "reservas"

    id_reserva= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id_biblioteca = Column(UUID(as_uuid=True), ForeignKey("bibliotecas.id_biblioteca"), nullable=True)
    fecha_reserva= Column(Date, nullable=True)
    estado= Column(String(50), nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    
    cod_cliente= Column(UUID(as_uuid=True), ForeignKey("clientes.codigo"))
    id_material= Column(UUID(as_uuid=True), ForeignKey("materiales.id_material"))

    id_usuario_crea = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True)
    id_usuario_edita = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True)

    cliente= relationship("Cliente", back_populates="reservas", foreign_keys=[cod_cliente])
    material= relationship("Material_Bibliografico", back_populates="reservas", foreign_keys=[id_material])
    biblioteca = relationship("Biblioteca")

    usuario_crea= relationship("Usuario", foreign_keys=[id_usuario_crea], overlaps="usuario_edita")
    usuario_edita= relationship("Usuario", foreign_keys=[id_usuario_edita], overlaps="usuario_crea")

    def __repr__(self):
        return f"<Reserva(id={self.id_reserva}, fecha_reserva={self.fecha_reserva}, estado='{self.estado}')>"