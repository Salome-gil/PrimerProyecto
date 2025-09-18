class Sede:
    """
    Representa una sede de la biblioteca.
    """

    def _init_(self, id: int, nombre: str, direccion: str):
        """
        Inicializa una nueva sede.

        Args:
            id (int): Identificador único de la sede.
            nombre (str): Nombre de la sede.
            direccion (str): Dirección física de la sede.
        """
        self.id= id
        self.nombre = nombre
        self.direccion = direccion
        self.biblioteca = None

    def _str_(self) -> str:
        """
        Representación en cadena de la sede.

        Returns:
            str: Información detallada de la sede (ID, nombre y dirección).
        """
        return f"ID: {self.id}, Sede: {self.nombre}, Dirección: {self.direccion}"