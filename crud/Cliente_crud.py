from typing import List, Optional
from uuid import UUID
from entities.Cliente import Cliente
from sqlalchemy.orm import Session


class ClienteCRUD:
    """
    Clase para realizar operaciones CRUD sobre clientes en la base de datos.
    """

    def __init__(self, db: Session):
        """
        Inicializa el CRUD con una sesión de base de datos.

        :param db: Sesión de SQLAlchemy para interactuar con la base de datos.
        :type db: Session
        """
        self.db = db

    def crear_cliente(self, nombre: str, tipo_cliente: str, detalle_tipo: str, id_biblioteca: UUID, id_usuario_crea: UUID = None) -> Cliente:
        """
        Crea un nuevo cliente en la base de datos.

        Args:
            nombre (str): Nombre del cliente.
            tipo_cliente (str): Tipo de cliente (ej. estudiante, profesor).
            detalle_tipo (str): Detalle adicional sobre el tipo de cliente.
            id_biblioteca (UUID): Identificador único de la biblioteca asociada.
            id_usuario_crea (UUID, opcional): Usuario que crea el cliente. 
                Si no se especifica, se asigna un administrador por defecto.

        Returns:
            Cliente: Objeto del cliente creado.

        Raises:
            ValueError: Si algún campo obligatorio no cumple las validaciones.
        """

        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre del cliente es obligatorio")
        if len(nombre) > 150:
            raise ValueError("El nombre no puede exceder 150 caracteres")
        
        if not tipo_cliente or len(tipo_cliente.strip()) == 0:
            raise ValueError("El tipo de cliente es obligatorio")

        if not detalle_tipo or len(detalle_tipo.strip()) == 0:
            raise ValueError("El detalle del tipo es obligatorio")
        
        from entities.Biblioteca import Biblioteca

        biblioteca = (self.db.query(Biblioteca).filter(Biblioteca.id_biblioteca == id_biblioteca).first())
        if not biblioteca:
            raise ValueError("La biblioteca especificada no existe")

        if id_usuario_crea is None:
            from entities.Usuario import Usuario

            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para crear el cliente"
                )
            id_usuario_crea = admin.id_usuario

        cliente = Cliente(
            nombre= nombre.strip(),
            tipo_cliente= tipo_cliente.strip(),
            detalle_tipo= detalle_tipo.strip(),
            vetado= False,
            id_biblioteca= id_biblioteca,
            id_usuario_crea=id_usuario_crea,
        )

        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def obtener_cliente(self, codigo: UUID, id_biblioteca: UUID) -> Optional[Cliente]:
        """
        Obtiene un cliente específico por su código y biblioteca.

        Args:
            codigo (UUID): Identificador único del cliente.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            Optional[Cliente]: Cliente encontrado o None si no existe.
        """
        return(self.db.query(Cliente).filter(Cliente.codigo == codigo, Cliente.id_biblioteca == id_biblioteca).first())

    def obtener_clientes(self, id_biblioteca: UUID, skip: int = 0, limit: int = 100) -> List[Cliente]:
        """
        Obtiene una lista de clientes de una biblioteca con paginación.

        Args:
            id_biblioteca (UUID): Identificador único de la biblioteca.
            skip (int, opcional): Número de registros a omitir. Por defecto 0.
            limit (int, opcional): Número máximo de registros a retornar. Por defecto 100.

        Returns:
            List[Cliente]: Lista de clientes encontrados.
        """
        return (self.db.query(Cliente).filter(Cliente.id_biblioteca == id_biblioteca).all())

    def obtener_clientes_por_nombre(self, nombre: str, id_biblioteca: UUID) -> List[Cliente]:
        """
        Busca clientes por nombre en una biblioteca.

        Args:
            nombre (str): Nombre del cliente.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            List[Cliente]: Lista de clientes con ese nombre.
        """
        return (self.db.query(Cliente).filter(Cliente.nombre == nombre, Cliente.id_biblioteca == id_biblioteca).all())

    def obtener_clientes_por_tipo_cliente(self, tipo_cliente: str, id_biblioteca: UUID) -> List[Cliente]:
        """
        Busca clientes por tipo en una biblioteca.

        Args:
            tipo_cliente (str): Tipo de cliente (ej. estudiante, profesor).
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            List[Cliente]: Lista de clientes que coinciden con ese tipo.
        """
        return self.db.query(Cliente).filter(Cliente.tipo_cliente == tipo_cliente, Cliente.id_biblioteca == id_biblioteca).all()

    def obtener_clientes_por_detalle_tipo(self, detalle_tipo: str, id_biblioteca: UUID) -> List[Cliente]:
        """
        Busca clientes por detalle del tipo en una biblioteca.

        Args:
            detalle_tipo (str): Descripción o detalle del tipo de cliente.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            List[Cliente]: Lista de clientes que coinciden con ese detalle.
        """
        return self.db.query(Cliente).filter(Cliente.detalle_tipo == detalle_tipo, Cliente.id_biblioteca == id_biblioteca).all()
    
    def obtener_clientes_por_vetado(self, vetado: bool, id_biblioteca: UUID) -> List[Cliente]:
        """
        Obtiene clientes según su estado de veto.

        Args:
            vetado (bool): Estado de veto (True o False).
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            List[Cliente]: Lista de clientes según el estado de veto.
        """
        return self.db.query(Cliente).filter(Cliente.vetado == vetado, Cliente.id_biblioteca == id_biblioteca).all()

    def actualizar_cliente(self, codigo: UUID, id_biblioteca: UUID, id_usuario_edita: UUID  = None, **kwargs) -> Optional[Cliente]:
        """
        Actualiza los datos de un cliente.

        Args:
            codigo (UUID): Identificador único del cliente.
            id_biblioteca (UUID): Identificador único de la biblioteca.
            id_usuario_edita (UUID, opcional): Usuario que edita el cliente. 
                Si no se especifica, se asigna un administrador por defecto.
            **kwargs: Campos a actualizar (ej. nombre, tipo_cliente, detalle_tipo, vetado).

        Returns:
            Optional[Cliente]: Cliente actualizado o None si no existe.

        Raises:
            ValueError: Si algún valor enviado es inválido.
        """

        cliente = (self.db.query(Cliente).filter(Cliente.codigo == codigo, Cliente.id_biblioteca == id_biblioteca).first())

        if not cliente:
            return None
        
        if "nombre" in kwargs:
            nombre = kwargs["nombre"]
            if not nombre or len(nombre.strip()) == 0:
                raise ValueError("El nombre del cliente es obligatorio")
            if len(nombre) > 150:
                raise ValueError("El nombre no puede exceder 150 caracteres")
            kwargs["nombre"] = nombre.strip()

        if "tipo_cliente" in kwargs:
            tipo = kwargs["tipo_cliente"]
            if not tipo or len(tipo.strip()) == 0:
                raise ValueError("El tipo de cliente es obligatorio")
            kwargs["tipo_cliente"] = tipo.strip()

        if "detalle_tipo" in kwargs:
            detalle = kwargs["detalle_tipo"]
            if not detalle or len(detalle.strip()) == 0:
                raise ValueError("El detalle del tipo es obligatorio")
            kwargs["detalle_tipo"] = detalle.strip()

        if "vetado" in kwargs:
            vetado = kwargs["vetado"]
            if not isinstance(vetado, bool):
                raise ValueError("El campo 'vetado' debe ser True o False")

        if id_usuario_edita is None:
            from entities.Usuario import Usuario
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError("No se encontró un usuario administrador para editar el cliente")
            id_usuario_edita = admin.id_usuario

        cliente.id_usuario_edita = id_usuario_edita

        for key, value in kwargs.items():
            if hasattr(cliente, key):
                setattr(cliente, key, value)

        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def actualizar_tipo_cliente(self, codigo: UUID, tipo_cliente: str, id_biblioteca: UUID) -> Optional[Cliente]:
        """
        Actualiza solo el tipo de un cliente.

        Args:
            codigo (UUID): Identificador único del cliente.
            tipo_cliente (str): Nuevo tipo de cliente.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            Optional[Cliente]: Cliente actualizado o None si no existe.

        Raises:
            ValueError: Si el tipo de cliente es inválido.
        """

        if not tipo_cliente or len(tipo_cliente.strip()) == 0:
            raise ValueError("El tipo de cliente es obligatorio")
        if len(tipo_cliente) > 50:
            raise ValueError("El tipo de cliente no puede exceder 50 caracteres")
    
        return self.actualizar_cliente(codigo, id_biblioteca=id_biblioteca, tipo_cliente=tipo_cliente)
    
    def actualizar_detalle_tipo(self, codigo: UUID, detalle_tipo: str, id_biblioteca: UUID) -> Optional[Cliente]:
        """
        Actualiza solo el detalle del tipo de un cliente.

        Args:
            codigo (UUID): Identificador único del cliente.
            detalle_tipo (str): Nuevo detalle del tipo.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            Optional[Cliente]: Cliente actualizado o None si no existe.

        Raises:
            ValueError: Si el detalle excede el límite permitido.
        """
        if detalle_tipo and len(detalle_tipo.strip()) > 100:
            raise ValueError("El detalle del tipo no puede exceder 100 caracteres")
    
        return self.actualizar_cliente(codigo, id_biblioteca=id_biblioteca, detalle_tipo=detalle_tipo)
    
    def actualizar_vetado(self, codigo: UUID, vetado: bool, id_biblioteca: UUID) -> Optional[Cliente]:
        """
        Actualiza el estado de veto de un cliente.

        Args:
            codigo (UUID): Identificador único del cliente.
            vetado (bool): Nuevo estado de veto.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            Optional[Cliente]: Cliente actualizado o None si no existe.
        """
        return self.actualizar_cliente(codigo, id_biblioteca=id_biblioteca, vetado=vetado)

    def eliminar_cliente(self, codigo: UUID, id_biblioteca: UUID) -> bool:
        """
        Elimina un cliente por su ID y biblioteca.

        Args:
            codigo (UUID): Identificador único del cliente.
            id_biblioteca (UUID): Identificador único de la biblioteca.

        Returns:
            bool: True si el cliente fue eliminado, False si no existe.
        """
        cliente = self.obtener_cliente(codigo, id_biblioteca)
        if cliente:
            self.db.delete(cliente)
            self.db.commit()
            return True
        return False