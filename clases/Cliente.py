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


#------------------------------------------------------------------------------------- 
# Herencia - Estudiante
#------------------------------------------------------------------------------------- 

class Estudiante(Cliente):
    # Clase Estudiante que hereda de Cliente y agrega el atributo "carrera".
    # Constructor de la clase Estudiante y llama al constructor de la clase padre (Cliente)

    def __init__(self, codigo: int, nombre: str, carrera: str, vetado: bool= False) -> None:
        super().__init__(codigo, nombre, vetado)
        self.__carrera= carrera

    # Retorna la carrera del estudiante.
    def get_carrera(self) -> str:
        return self.__carrera
    
    # Asigna una nueva carrera al estudiante.
    def set_carrera(self, carrera: str) -> None:
        self.__carrera = carrera

    # Método polimórfico: sobrescribe el método para indicar que es Estudiante.
    def tipo_cliente(self) -> str:
        return "Estudiante"
    
    # toString() - retorna una cadena de un estudiante.
    def __str__(self) -> str:
        return super().__str__() + f", Clasificación: {self.tipo_cliente()}, Carrera: {self.__carrera}"


#------------------------------------------------------------------------------------- 
# Herencia - Profesor
#------------------------------------------------------------------------------------- 

class Profesor(Cliente):
    # Clase Profesor que hereda de Cliente y agrega el atributo "facultad".
    # Constructor de la clase Profesor y llama al constructor de la clase padre (Cliente)
    
    def __init__(self, codigo: int, nombre: str, facultad: str, vetado: bool= False) -> None:
        super().__init__(codigo, nombre, vetado)
        self.__facultad= facultad

    # Retorna la facultad del profesor.
    def get_facultad(self) -> str:
        return self.__facultad
    
    # Asigna una nueva facultad al profesor.
    def set_facultad(self, facultad: str) -> None:
        self.__facultad= facultad

    # Método polimórfico: sobrescribe el método para indicar que es Profesor. 
    def tipo_cliente(self) -> str:
        return "Profesor"
    
    # toString() - retorna una cadena de un Profesor.
    def __str__(self) -> str:
        return super().__str__() + f", Clasificación: {self.tipo_cliente()}, Facultad: {self.__facultad}"


#------------------------------------------------------------------------------------- 
# Herencia - Empleado
#------------------------------------------------------------------------------------- 

class Empleado(Cliente):
    # Clase Empleado que hereda de Cliente y agrega el atributo "cargo".
    # Constructor de la clase Empleado y llama al constructor de la clase padre (Cliente)

    def __init__(self, codigo: int, nombre: str, cargo: str, vetado: bool= False) -> None:
        super().__init__(codigo, nombre, vetado)
        self.__cargo= cargo
    
    # Retorna el cargo del empleado.
    def get_cargo(self) -> str:
        return self.__cargo

    # Asigna un nuevo cargo al empleado.
    def set_cargo(self, cargo: str) -> None:
        self.__cargo= cargo

    # Método polimórfico: sobrescribe el método para indicar que es Empleado.
    def tipo_cliente(self) -> str:
        return "Empleado"

    # toString() - retorna una cadena de un Empleado.
    def __str__(self) -> str:
        return super().__str__() + f", Clasificación: {self.tipo_cliente()}, Cargo: {self.__cargo}"