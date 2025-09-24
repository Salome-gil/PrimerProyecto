from Cliente import Cliente
from Material_Bibliografico import Material_Bibliografico
from datetime import date

class Prestamo:
    """
    Representa un préstamo de material bibliográfico realizado por un cliente.
    """

    def _init_(self, Id: int, cliente: Cliente, material: Material_Bibliografico, fecha_prestamo: date, fecha_entrega: date):
        """
        Inicializa un nuevo préstamo.

        Args:
            Id (int): Identificador único del préstamo.
            cliente (Cliente): Cliente que realiza el préstamo.
            material (Material_Bibliografico): Material bibliográfico prestado.
            fecha_prestamo (date): Fecha en la que se realizó el préstamo.
            fecha_entrega (date): Fecha límite de entrega del material.
        """
        self.Id = Id
        self.cliente = cliente
        self.material = material
        self.__fecha_prestamo = fecha_prestamo
        self.__fecha_entrega = fecha_entrega

    def get_fecha_prestamo(self) -> date:
        """
        Obtener la fecha del préstamo.

        Returns:
            date: Fecha en que se realizó el préstamo.
        """
        return self.__fecha_prestamo
    
    def set_fecha_prestamo(self, fecha_prestamo: date) -> None:
        """
        Establecer una nueva fecha de préstamo.

        Args:
            fecha_prestamo (date): Nueva fecha del préstamo.
        """
        self.__fecha_prestamo= fecha_prestamo

    def get_fecha_entrega(self) -> date:
        """
        Obtener la fecha de entrega del préstamo.

        Returns:
            date: Fecha límite para devolver el material.
        """
        return self.__fecha_entrega
    
    def set_fecha_entrega(self, fecha_entrega: date) -> None:
        """
        Establecer una nueva fecha de entrega.

        Args:
            fecha_entrega (date): Nueva fecha de devolución del material.
        """
        self.__fecha_entrega= fecha_entrega

    def _str_(self) -> str:
        """
        Representación en cadena del préstamo.

        Returns:
            str: Información detallada del préstamo (cliente, material y fechas).
        """
        return f"ID: {self.Id}, Cliente: {self.cliente.nombre}, Material Bibliográfico: {self.material.titulo}, Fecha del préstamo: {self._fecha_prestamo}, Fecha de entrega: {self._fecha_entrega}"

    def renovar_prestamo(self, nueva_fecha_entrega: date) -> None:
       """
        Renovar el préstamo cambiando la fecha de entrega.

        Args:
            nueva_fecha_entrega (date): Nueva fecha límite para devolver el material.
        """
       self.__fecha_entrega = nueva_fecha_entrega