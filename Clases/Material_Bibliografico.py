from Categoria import Categoria
from Sede import Sede
from typing import Optional

class Material_Bibliografico:
    """
    Representa un material bibliográfico en la biblioteca.
    """

    def _init_(self, Id: int, titulo: str, autor: str, categoria: Categoria, sede: Sede, estado: str):
        """
        Inicializa un nuevo material bibliográfico.

        Args:
            Id (int): Identificador único del material.
            titulo (str): Título del material bibliográfico.
            autor (str): Autor del material.
            categoria (Categoria): Categoría a la que pertenece el material.
            sede (Sede): Sede de la biblioteca donde se encuentra el material.
            estado (str): Estado del material (ej. 'disponible', 'prestado').
        """
        self.Id = Id
        self.titulo= titulo
        self.autor= autor
        self.categoria= categoria
        self.sede= sede
        self.__estado = estado

    def get_estado(self) -> str:
        """
        Obtener el estado actual del material.

        Returns:
            str: Estado del material (ej. 'disponible', 'prestado').
        """
        return self.__estado
    
    def set_estado(self, estado: str) -> None:
        """
        Establecer el estado del material.

        Args:
            estado (str): Nuevo estado del material.
        """
        self.__estado= estado

    def _str_(self) -> str:
        """
        Representación en cadena del material bibliográfico.

        Returns:
            str: Información detallada del material.
        """
        return f"Código: {self.Id}, Titulo: {self.titulo}, Autor: {self.autor}, Estado: {self.__estado}, Categoria: {self.categoria.nombre}, Biblioteca: Sede {self.sede.nombre}"

    def marcar_disponible(self) -> None:
        """
        Marcar el material como disponible.
        """
        self.__estado = "disponible"
    
    def marcar_no_disponible(self) -> None:
        """
        Marcar el material como no disponible (prestado).
        """
        self.__estado = "prestado"