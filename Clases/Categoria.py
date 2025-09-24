class Categoria:
    """
    Representa una categoría de material bibliográfico en la biblioteca.
    """
    
    def _init_(self, id_categoria: int, nombre: str, descripcion: str):
        """
        Inicializa una nueva categoría.

        Args:
            id_categoria (int): Identificador único de la categoría.
            nombre (str): Nombre de la categoría.
            descripcion (str): Descripción de la categoría.
        """
        self.id_categoria = id_categoria
        self.nombre = nombre
        self.descripcion = descripcion

    def _str_(self) -> str:
        """
        Representación en cadena de la categoría.

        Returns:
            str: Cadena con el ID, nombre y descripción de la categoría.
        """
        return f"ID: {self.id_categoria} - {self.nombre}, Descripción: {self.descripcion}"