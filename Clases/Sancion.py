from Cliente import Cliente
from datetime import date

class Sancion:
    """
    Representa una sanción impuesta a un cliente de la biblioteca.
    """

    def __init__(self, id_sancion: int, cliente: Cliente, motivo: str, fecha_sancion: date, monto: float):
        """
        Inicializa una nueva sanción.

        Args:
            id_sancion (int): Identificador único de la sanción.
            cliente (Cliente): Cliente al que se le aplica la sanción.
            motivo (str): Motivo de la sanción.
            fecha_sancion (date): Fecha en la que se registró la sanción.
            monto (float): Monto económico asociado a la sanción.
        """
        self.id_sancion = id_sancion
        self.cliente = cliente
        self.motivo = motivo
        self.fecha_sancion = fecha_sancion
        self.monto = monto

    def __str__(self) -> str:
        """
        Representación en cadena de la sanción.

        Returns:
            str: Información detallada de la sanción (cliente, motivo, fecha y monto).
        """
        return f"Sanción: {self.id_sancion}, Cliente: {self.cliente.codigo} - {self.cliente.nombre}, Motivo: {self.motivo}, Fecha: {self.fecha_sancion}, Monto: ${self.monto}"
