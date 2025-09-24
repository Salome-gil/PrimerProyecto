"""IDENTIDAD CLIENTE DE LA CLASE CLIENTE"""
import uuid
from sqlalchemy.dialects.postgresql import UUID
from database.config import Base
from sqlalchemy import Column, ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

"""ATRIBUTOS DE LA ENTIDAD:
    codigo: uuid, clave primaria
    nombre:nombre completo del cliente
    tipo_cliente: que tipo de cliente es: profesor, estudiante, trabajador
    detalle_tipo: si es profesor a que facultad pertenece, si es estudiante a que carrera pertenece, si es trabajador cual es el area de trabajo
    vetado: si el cliente esta vetado o no"""

class Cliente(Base):
    __tablename__ = "clientes"

    codigo= Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nombre= Column(String(80), nullable=True)
    tipo_cliente= Column(String(80), nullable=True)
    detalle_tipo= Column(String(80), nullable=True)
    vetado= Column(Boolean, default=False, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    
    id_biblioteca = Column(UUID(as_uuid=True), ForeignKey("bibliotecas.id_biblioteca"))

    id_usuario_crea = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True)
    id_usuario_edita = Column(UUID(as_uuid=True), ForeignKey("usuarios.id_usuario"), nullable=True)

    biblioteca = relationship("Biblioteca", back_populates="clientes")
    prestamos= relationship("Prestamo", back_populates="cliente")
    reservas= relationship("Reserva", back_populates="cliente")
    sanciones= relationship("Sancion", back_populates="cliente")

    usuario_crea= relationship("Usuario", foreign_keys=[id_usuario_crea], overlaps="usuario_edita")
    usuario_edita= relationship("Usuario", foreign_keys=[id_usuario_edita], overlaps="usuario_crea")

    def __repr__(self):
        return f"<Cliente(codigo={self.codigo}, nombre='{self.nombre}', tipo_cliente='{self.tipo_cliente}', detalle_tipo='{self.detalle_tipo}', vetado={self.vetado})>"
    