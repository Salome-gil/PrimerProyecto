class Cliente:
    """
    Representa un cliente de la biblioteca.
    """

    def _init_(self, codigo: int, nombre: str, tipo_cliente: str, detalle_tipo: str, vetado: bool= False):
        """
        Inicializa un nuevo cliente.

        Args:
            codigo (int): Código único del cliente.
            nombre (str): Nombre completo del cliente.
            tipo_cliente (str): Tipo de cliente (por ejemplo: estudiante, profesor, empleado).
            detalle_tipo (str): Detalle adicional del tipo de cliente (por ejemplo: carrera, facultad, cargo).
            vetado (bool, opcional): Estado inicial de veto del cliente. Por defecto es False.
        """
        self.codigo = codigo
        self.nombre = nombre
        self.tipo_cliente= tipo_cliente
        self.detalle_tipo= detalle_tipo
        self.__vetado = vetado

    def get_vetado(self) -> bool:
        """
        Obtener el estado de veto del cliente.

        Returns:
            bool: True si el cliente está vetado, False en caso contrario.
        """
        return self.__vetado
    
    def set_vetado(self, vetado: bool) -> None:
        """
        Establecer el estado de veto del cliente.

        Args:
            vetado (bool): Nuevo estado de veto.
        """
        self.__vetado= vetado
    
    def _str_(self) -> str:
        """
        Representación en cadena del cliente.

        Returns:
            str: Información completa del cliente en formato legible.
        """
        return f"Código: {self.codigo}, Nombre: {self.nombre}, Tipo de cliente: {self.tipo_cliente} - {self.detalle_tipo}, Vetado: {self.__vetado}" 

    def marcar_vetado(self) -> None:
        """
        Marcar al cliente como vetado.
        """
        self.__vetado = True

    def quitar_vetado(self) -> None:
        """
        Quitar el veto al cliente.
        """
        self.__vetado = False

    def es_vetado(self) -> bool:
        """
        Verificar si el cliente está vetado.

        Returns:
            bool: True si está vetado, False en caso contrario.
        """
        return self.__vetado
