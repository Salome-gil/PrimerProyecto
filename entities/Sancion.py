"""ENTIDAS SANCION DE LA CLASE SANCION"""
import uuid
from sqlalchemy.dialects.postgresql import UUID
from database.config import Base
from sqlalchemy import Column, Date, ForeignKey, Numeric, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

"""ATRIBUTOS DE LA ENTIDAD:
    id_sancion: uuid, clave primaria
    id_biblioteca: clave foranea de la entidad biblioteca
    motivo: breve descipcion del por que se sanciona al cliente
    monto: dinero a pagar por la sancion
    fecha: fecha en la cual fue emitida la sancion
    cod_cliente: clave foranea de la entidad cliente"""

class Sancion(Base):
    __tablename__ = "sanciones"

    id_sancion= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id_biblioteca = Column(UUID(as_uuid=True), ForeignKey("bibliotecas.id_biblioteca"), nullable=True)
    motivo= Column(String(150), nullable=True)
    fecha_sancion= Column(Date, nullable=True)
    monto= Column(Numeric(10, 2), nullable=True)
    cod_cliente= Column(UUID(as_uuid=True), ForeignKey("clientes.codigo"))
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    id_usuario_crea = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True)
    id_usuario_edita = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True)

    cliente= relationship("Cliente", back_populates="sanciones", foreign_keys=[cod_cliente])
    biblioteca = relationship("Biblioteca")

    usuario_crea= relationship("Usuario", foreign_keys=[id_usuario_crea], overlaps="usuario_edita")
    usuario_edita= relationship("Usuario", foreign_keys=[id_usuario_edita], overlaps="usuario_crea")

    def __repr__(self):
        return f"<Sancion(id_sancion={self.id_sancion}, motivo='{self.motivo}', fecha_sancion={self.fecha_sancion}, monto={self.monto})>"