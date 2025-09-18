from datetime import date
from Cliente import Cliente 
from Material_Bibliografico import Material_Bibliografico

class Reserva:
    """
    Representa una reserva de un material bibliográfico realizada por un cliente.
    """

    def __init__(self, id: int, cli: Cliente, mat: Material_Bibliografico, fecha_reserva: date, estado: str):
        """
        Inicializa una nueva reserva.

        Args:
            id (int): Identificador único de la reserva.
            cli (Cliente): Cliente que realiza la reserva.
            mat (Material_Bibliografico): Material bibliográfico reservado.
            fecha_reserva (date): Fecha en la que se realizó la reserva.
            estado (str): Estado de la reserva (ej. 'activa', 'cancelada', 'atendida').
        """
        self.id= id
        self.cli= cli
        self.mat= mat
        self.fecha_reserva= fecha_reserva
        self.__estado= estado

    def get_estado(self) -> str:
        """
        Obtener el estado de la reserva.

        Returns:
            str: Estado actual de la reserva.
        """
        return self.__estado
    
    def set_estado(self, estado) -> None:
        """
        Establecer un nuevo estado para la reserva.

        Args:
            estado (str): Nuevo estado de la reserva.
        """
        self.__estado= estado

    def __str__(self) -> str:
        """
        Representación en cadena de la reserva.

        Returns:
            str: Información detallada de la reserva (cliente, material, fecha y estado).
        """
        return (f"ID: {self.id}, Cliente: {self.cli.nombre}, Material: {self.mat.titulo}, Fecha: {self.fecha_reserva}, Estado: {self.__estado}")
        
    