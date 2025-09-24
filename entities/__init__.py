"""
Módulo entities.

Este paquete contiene las definiciones de las entidades del sistema,
correspondientes a las tablas de la base de datos. Cada entidad es
una clase que representa un modelo de SQLAlchemy.

Entidades disponibles:
    - Biblioteca
    - Categoria
    - Cliente
    - Material_Bibliografico
    - Prestamo
    - Reserva
    - Sancion
    - Usuario
    - Sede
"""

from .Biblioteca import   Biblioteca
from .Categoria import Categoria
from .Cliente import Cliente
from .Material_Bibliografico import Material_Bibliografico
from .Prestamo import Prestamo
from .Reserva import Reserva
from .Sancion import Sancion
from .Usuario import Usuario
from .Sede import Sede