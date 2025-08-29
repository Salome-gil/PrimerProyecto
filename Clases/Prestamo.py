from datetime import date

class Prestamo:
    def __init__(self, Id: int, cod_cliente: int, cod_material: int, fecha_prestamo: date, fecha_entrega: date):
        self.__Id = Id
        self.__cod_cliente = cod_cliente
        self.__cod_material = cod_material
        self.__fecha_prestamo = fecha_prestamo
        self.__fecha_entrega = fecha_entrega

    def get_id(self) -> int:
        return self.__Id
    
    def set_id(self, id: int) -> None:
        self.__Id= id

    def get_cod_cliente(self) -> int:
        return self.__cod_cliente
    
    def set_cod_cliente(self, cod_cliente: int) -> None:
        self.__cod_cliente= cod_cliente

    def get_cod_material(self) -> int:
        return self.__cod_material
    
    def set_cod_material(self, cod_material: int) -> None:
        self.__cod_material= cod_material

    def get_fecha_prestamo(self) -> date:
        return self.__fecha_prestamo
    
    def set_fecha_prestamo(self, fecha_prestamo: date) -> None:
        self.__fecha_prestamo= fecha_prestamo

    def get_fecha_entrega(self) -> date:
        return self.__fecha_entrega
    
    def set_fecha_entrega(self, fecha_entrega: date) -> None:
        self.__fecha_entrega= fecha_entrega

    def __str__(self) -> str:
        return f"Código: {self.__Id}, Código cliente: {self.__cod_cliente}, Código material bibliográfico: {self.__cod_material}, Fecha del préstamo: {self.__fecha_prestamo}, Fecha de entrega: {self.__fecha_entrega}"