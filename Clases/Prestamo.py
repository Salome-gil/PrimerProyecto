from datetime import date

class Prestamo:

    # Constructor de la clase Prestamo, con atributos privados
    def __init__(self, Id: int, cod_cliente: int, cod_material: int, fecha_prestamo: date, fecha_entrega: date) -> None:
        self.__Id = Id
        self.__cod_cliente = cod_cliente
        self.__cod_material = cod_material
        self.__fecha_prestamo = fecha_prestamo
        self.__fecha_entrega = fecha_entrega

    # Obtiene el ID del préstamo.
    def get_id(self) -> int:
        return self.__Id
    
    # Modifica el ID del préstamo.
    def set_id(self, id: int) -> None:
        self.__Id= id

    # Obtiene el código del cliente asociado al préstamo.
    def get_cod_cliente(self) -> int:
        return self.__cod_cliente
    
    # Modifica el código del cliente asociado al préstamo.
    def set_cod_cliente(self, cod_cliente: int) -> None:
        self.__cod_cliente= cod_cliente

    # Obtiene el código del material bibliográfico prestado.
    def get_cod_material(self) -> int:
        return self.__cod_material
    
    # Modifica el código del material bibliográfico prestado.
    def set_cod_material(self, cod_material: int) -> None:
        self.__cod_material= cod_material

    # Obtiene la fecha en que se realizó el préstamo.
    def get_fecha_prestamo(self) -> date:
        return self.__fecha_prestamo
    
    # Modifica la fecha en que se realizó el préstamo.
    def set_fecha_prestamo(self, fecha_prestamo: date) -> None:
        self.__fecha_prestamo= fecha_prestamo

    # Obtiene la fecha de entrega pactada del préstamo.
    def get_fecha_entrega(self) -> date:
        return self.__fecha_entrega
    
    # Modifica la fecha de entrega pactada del préstamo.
    def set_fecha_entrega(self, fecha_entrega: date) -> None:
        self.__fecha_entrega= fecha_entrega

    # toString() - Representación en cadena del préstamo.
    def __str__(self) -> str:
        return f"Código: {self.__Id}, Código cliente: {self.__cod_cliente}, Código material bibliográfico: {self.__cod_material}, Fecha del préstamo: {self.__fecha_prestamo}, Fecha de entrega: {self.__fecha_entrega}"

#------------------------------------------------------------------------------------- 
# Métodos adicionales de para el prestamo
#------------------------------------------------------------------------------------- 

    # Renueva el préstamo modificando la fecha de entrega.
    def renovar_prestamo(self, nueva_fecha_entrega: date) -> None:
       self.__fecha_entrega = nueva_fecha_entrega

    # Verifica si el préstamo ya está vencido.
    def es_vencido(self, fecha_actual: date) -> bool:
        return fecha_actual > self.__fecha_entrega

    # Calcula los días de atraso en la entrega.
    def dias_atraso(self, fecha_actual: date) -> int:
        if fecha_actual > self.__fecha_entrega:
            return (fecha_actual - self.__fecha_entrega).days
        return 0

    # Verifica si el préstamo pertenece a un cliente específico.
    def pertenece_a_cliente(self, cod_cliente: int) -> bool:
        return self.__cod_cliente == cod_cliente

    # Verifica si el préstamo corresponde a un material específico.
    def es_del_material(self, cod_material: int) -> bool:
        return self.__cod_material == cod_material