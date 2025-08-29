from typing import Optional

class Material_Bibliografico:

    # Constructor de la clase Material Bibliográfico, con atributos privados
    def __init__(self, Id: int, estado: str, cliente_reserva: Optional[int], reservado: bool= False) -> None:
        self.__Id = Id
        self.__estado = estado
        self.__cliente_reserva = cliente_reserva
        self.__reservado = reservado

#------------------------------------------------------------------------------------------
#  ENCAPSULADOS (Getters y Setters)
#-----------------------------------------------------------------------------------------    

    # Métodos para acceder y modificar los atributos privados de la clase.
    def get_Id(self) -> int:
        return self.__Id
    
    def set_Id(self, Id: int) -> None:
        self.__Id= Id

    def get_estado(self) -> str:
        return self.__estado
    
    def set_estado(self, estado: str) -> None:
        self.__estado= estado

    def get_cliente_reserva(self) -> Optional[int]:
        return self.__cliente_reserva
    
    def set_cliente_reserva(self, cliente_reserva: int) -> None:
        self.__cliente_reserva= cliente_reserva

    def get_reservado(self) -> bool:
        return self.__reservado
    
    def set_reservado(self, reservado: bool) -> None:
        self.__reservado= reservado

#------------------------------------------------------------------------------------------
#  RESERVAR MATERIAL
#-----------------------------------------------------------------------------------------    
    
    # Permite reservar el material si está disponible y no tiene una reserva activa.
    def reservar(self, cod_cliente: int) -> bool:
        if self.__estado == "disponible":  # Solo se permite reservar el material si está disponible
            if not self.__reservado:
                return True  # si la reserva se realizó correctamente.
            else:
                return False 
        else: 
            return False  # si no fue posible realizar la reserva.

#------------------------------------------------------------------------------------------
#  CANCELAR RESERVA DEL MATERIAL
#-----------------------------------------------------------------------------------------    

    # Cancela la reserva si el cliente que la hizo coincide con el que intenta cancelarla.
    def cancelar_reserva(self, cod_cliente: int) -> bool:
        if self.__reservado and self.__cliente_reserva == cod_cliente:  # Compara el cod del cliente que hizo la reserva con el que intenta cancelarla
            return True  # si la reserva fue cancelada exitosamente.
        elif self.__reservado:
            return False  # si la reserva no puede ser cancelada (otro cliente la reservó).
        else:
            return False  # si la reserva no puede ser cancelada (no está reservada).