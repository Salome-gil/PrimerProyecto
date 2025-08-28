class Cliente:

# Constructor de la clase Cliente, con atributos privados
    def __init__(self, codigo: int, nombre: str, vetado: bool= False) -> None:
        self.__codigo = codigo
        self.__nombre = nombre
        self.__vetado = vetado

#------------------------------------------------------------------------------------- 
# Getters y Setters
#------------------------------------------------------------------------------------- 

    # Retorna el código del cliente.
    def get_codigo(self) -> int:
        return self.__codigo
    
    # Asigna un nuevo código al cliente.
    def set_codigo(self, codigo: int) -> None:
        self.__codigo= codigo

    # Retorna el nombre del cliente.
    def get_nombre(self) -> str:
        return self.__nombre
    
    # Asigna un nuevo nombre al cliente.
    def set_nombre(self, nombre: str)-> None:
        self.__nombre= nombre

    # Retorna el estado de vetado del cliente.
    def get_vetado(self) -> bool:
        return self.__vetado
    
    # Cambia el estado de vetado del cliente.
    def set_vetado(self, vetado: bool) -> None:
        self.__vetado= vetado
    
    # PolimorfismoMétodo polimórfico: sobrescribe el método para indicar que es Cliente genérico
    def tipo_cliente(self) -> str:
        return "Cliente genérico"
    
    # toString() - retorna una cadena de un cliente.
    def __str__(self) -> str:
        return f"Código: {self.__codigo}, Nombre: {self.__nombre}, Vetado: {self.__vetado}" 
    
#------------------------------------------------------------------------------------- 
# Métodos adicionales de control de vetado
#------------------------------------------------------------------------------------- 

    # Marca al cliente como vetado.
    def marcar_vetado(self) -> None:
        self.__vetado = True

    # Quita el veto al cliente.
    def quitar_vetado(self) -> None:
        self.__vetado = False

    # Indica si el cliente está vetado.
    def es_vetado(self) -> bool:
        return self.__vetado