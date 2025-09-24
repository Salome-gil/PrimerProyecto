"""
Módulo de gestión de biblioteca

Contiene la clase `Biblioteca`, que administra clientes, materiales bibliográficos,
préstamos, reservas, sanciones y categorías. Permite realizar operaciones de
agregar, buscar, listar, prestar, devolver, reservar y sancionar.
"""

from typing import List, Optional
from Cliente import Cliente 
from Material_Bibliografico import Material_Bibliografico
from Prestamo import Prestamo
from Reserva import Reserva
from Sancion import Sancion
from Categoria import Categoria
from datetime import date, timedelta
from tkinter import messagebox, simpledialog

class Biblioteca:

    def __init__(self, nombre: str):
        """
        Inicializa una nueva instancia de Biblioteca.

        Args:
            nombre (str): Nombre de la biblioteca.
        """
        self.nombre = nombre
        self._clientes: List[Cliente] = []
        self._materiales: List[Material_Bibliografico] = []
        self._prestamos: List[Prestamo] = []
        self._reservas: List[Reserva] = []
        self._sanciones: List[Sancion] = []
        self._categorias: List[Categoria] = []

        self._contador_prestamos: int = 0
        self._contador_reservas: int = 0
        self._contador_sanciones: int = 0


    def agregar_cliente(self, cliente: Cliente) -> None:
        """
        Agrega un cliente a la biblioteca.

        Args:
            cliente: Instancia de Cliente a agregar.

        Raises:
            ValueError: Si ya existe un cliente con el mismo código.
        """
        for cli in self._clientes: 
            if cli.codigo == cliente.codigo:
                messagebox.showerror("Error", f"El cliente con código {cliente.codigo} ya existe.")
                return
        self._clientes.append(cliente)
        messagebox.showinfo("Exito", f"Cliente {cliente.nombre} agregado correctamente.")
    

    def agregar_material(self, material: Material_Bibliografico) -> None:
        """
        Agrega un material bibliográfico.

        Args:
            material: Instancia de Material_Bibliografico a agregar.

        Raises:
            ValueError: Si ya existe un material con el mismo ID.
        """
        for mat in self._materiales: 
            if mat.Id == material.Id:
                messagebox.showerror("Error", f"El material bibliografico con ID {material.Id} ya existe.")
                return 
        self._materiales.append(material)
        messagebox.showinfo("Exito", f"Material {material.titulo} agregado correctamente.")


    def agregar_categoria(self, categoria: Categoria) -> None:
        """
        Agrega una categoría.

        Args:
            categoria: Instancia de Categoria a agregar.

        Raises:
            ValueError: Si ya existe una categoría con el mismo ID.
        """
        for cat in self._categorias:
            if cat.id_categoria == categoria.id_categoria:
                messagebox.showerror("Error", f"La categoria con ID {categoria.id_categoria} ya existe.")
                return
        self._categorias.append(categoria)
        messagebox.showinfo("Exito", f"Categoria {categoria.nombre} agregada correctamente.")


    def agregar_sancion(self, cliente: Cliente, motivo: str, monto: float) -> None:
        """
        Registra una sanción para un cliente.

        Args:
            cliente: Cliente sancionado.
            motivo: Razón de la sanción.
            monto: Monto económico de la sanción.
        """
        self._contador_sanciones += 1

        sancion= Sancion(self._contador_sanciones, cliente, motivo, date.today(), monto)
        cliente.marcar_vetado()

        self._sanciones.append(sancion)
        messagebox.showinfo("Éxito", f"Sanción {sancion.id_sancion} agregada correctamente.")


    def buscar_cliente(self, buscar_cod: int) -> None:
        """
        Busca un cliente por código.

        Args:
            buscar_cod: Código del cliente.
        """
        for cli in self._clientes:  
            if cli.codigo == buscar_cod:  
                messagebox.showinfo("Éxito", f"Cliente encontrado:\n{cli}.")
                return  
        messagebox.showerror("Error", f"No se encontró un cliente con ID {buscar_cod}.")    
    

    def buscar_material(self, buscar_cod: int) -> None:
        """
        Busca un material bibliográfico por ID.

        Args:
            buscar_cod: ID del material bibliográfico.
        """
        for mat in self._materiales:  
            if mat.Id == buscar_cod:  
                messagebox.showinfo("Éxito", f"Material bibliografico encontrado:\n{mat}.")
                return  
        messagebox.showerror("Error",f"No se encontró material bibliografico con ID {buscar_cod}.")


    def buscar_prestamo(self, buscar_cod: int) -> None:
        """
        Busca un prestamo por ID.

        Args:
            buscar_cod: ID del prestamo.
        """
        for pre in self._prestamos:  
            if pre.Id == buscar_cod:  
                messagebox.showinfo("Éxito", f"Prestamo encontrado:\n{pre}.")
                return  
        messagebox.showerror("Error", f"No se encontró prestamo con ID {buscar_cod}.")


    def buscar_reserva(self, buscar_cod: int) -> None:
        """
        Busca una reserva por ID.

        Args:
            buscar_cod: ID de la reserva.
        """
        for res in self._reservas:
            if res.id == buscar_cod:
                messagebox.showinfo("Éxito", f"Reserva encontrada:\n{res}.")
                return
        messagebox.showerror("Error", f"No se encontró reserva con ID {buscar_cod}.")


    def buscar_sancion(self, buscar_cod: int) -> None:
        """
        Busca una sanción por ID.

        Args:
            buscar_cod: ID de la sanción.
        """
        for san in self._sanciones:
            if san.id_sancion == buscar_cod:
                messagebox.showinfo("Éxito", f"Sanción encontrada:\n{san}")
                return
        messagebox.showerror("Error", f"No se encontró sanción con ID {buscar_cod}")    


    def ver_clientes(self) -> None:
        """
        Muestra todos los clientes registradas.
        """
        if not self._clientes: 
            messagebox.showerror("Error", "No hay clientes registrados.")
            return 
        
        lista = "\n".join(str(cli) for cli in self._clientes) 
        messagebox.showinfo("Listado de Clientes", lista) 
    

    def ver_materiales(self) -> None:
        """
        Muestra todos los materiales registradas.
        """
        if not self._materiales: 
            messagebox.showerror("Error", "No hay materiales bibliográficos registrados.")
            return 
        
        lista = "\n".join(str(mat) for mat in self._materiales) 
        messagebox.showinfo("Listado de Materiales Bibliográficos", lista)
    

    def ver_prestamos(self) -> None:
        """
        Muestra todos los préstamos registradas.
        """
        if not self._prestamos: 
            messagebox.showerror("Error", "No hay préstamos registrados.")
            return 
        
        lista= "\n".join(str(pre) for pre in self._prestamos)
        messagebox.showinfo("Listado de Préstamos", lista)
    

    def ver_reservas(self) -> None:
        """
        Muestra todas las reservas registradas.
        """
        if not self._reservas:
            messagebox.showerror("Error", "No hay reservas registradas.")
            return 
        
        lista= "\n".join(str(res) for res in self._reservas)
        messagebox.showinfo("Listado de Reservas", lista)


    def ver_sanciones(self) -> None:
        """
        Muestra todas las sanciones registradas.
        """
        if not self._sanciones:
            messagebox.showerror("Error", "No hay sanciones registradas.")
            return 
        
        lista= "\n".join(str(san) for san in self._sanciones)
        messagebox.showinfo("Listado de Sanciones", lista)


    def ver_categorias(self) -> None:
        """
        Muestra todas las categorías registradas.
        """
        if not self._categorias:
            messagebox.showerror("Error", "No hay categorías registradas.")
            return 
        
        lista= "\n".join(str(cat) for cat in self._categorias)
        messagebox.showinfo("Listado de Categorías", lista)


    def prestar_material(self, cod_cliente: int, cod_material: int) -> bool:
        """
        Realiza un préstamo de material a un cliente.

        Args:
            cod_cliente: Código del cliente.
            cod_material: ID del material.

        Returns:
            True si el préstamo fue exitoso, False en caso contrario.
        """
        cliente: Optional[Cliente] = None
        for cli in self._clientes:
            if cli.codigo == cod_cliente:
                cliente= cli
                break

        if cliente is None:
            messagebox.showerror("Error", f"No existe un cliente con código {cod_cliente}.")
            return False
        
        if cliente.es_vetado():
            messagebox.showerror("Error", f"El cliente {cliente.nombre} está vetado.")
            return False

        material: Optional[Material_Bibliografico] = None
        for mat in self._materiales:
            if mat.Id == cod_material:
                material = mat
                break

        if material is None:
            messagebox.showerror("Error", f"No existe material bibliográfico con código {cod_material}.")
            return False
        
        reserva: Optional[Reserva]= None
        for res in self._reservas:
            if res.mat.Id == cod_material:
                reserva= res
                break
        
        if reserva is not None:
            if reserva.cli.codigo != cod_cliente:
                messagebox.showerror("Error", f"El material {material.Id} está reservado por otro cliente")
                return False
            else:
                self._reservas.remove(reserva)

        if material.get_estado() != "disponible":
            messagebox.showerror("Error", f"El material bibliográfico {material.Id} no está disponible.")
            return False
        
        self._contador_prestamos += 1
        nuevo_id = self._contador_prestamos

        fecha_prestamo = date.today()
        fecha_entrega = fecha_prestamo + timedelta(days=7)

        prestamo = Prestamo(nuevo_id, cliente, material, fecha_prestamo, fecha_entrega)
        self._prestamos.append(prestamo)

        material.marcar_no_disponible()

        messagebox.showinfo("Préstamo creado con exito", f"Préstamo creado. ID={nuevo_id}, Cliente={cliente.nombre}, Fecha de entrega {fecha_entrega}")
        return True


    def renovar_prestamo(self, cod_cliente: int, cod_material: int) -> bool:
        """
        Renueva un préstamo existente.

        Args:
            cod_cliente: Código del cliente.
            cod_material: ID del material.

        Returns:
            True si la renovación fue exitosa, False en caso contrario.
        """
        cliente:Optional[Cliente] = None
        for cli in self._clientes:
            if cli.codigo == cod_cliente:
                cliente= cli
                break

        if cliente is None:
            messagebox.showerror("Error", f"No existe cliente con ID {cod_cliente}.")
            return False
        
        if cliente.es_vetado():
            messagebox.showerror("Error", f"El cliente {cliente.nombre} con ID {cod_cliente} se encuentra vetado.")
            return False

        material: Optional[Material_Bibliografico] = None
        for mat in self._materiales:
            if mat.Id == cod_material:
                material= mat
                break

        if material is None:
            messagebox.showerror("Error", f"No existe material bibliografico con ID {cod_material}.")
            return False
        
        for reserva in self._reservas:
            if reserva.mat.Id == cod_material and reserva.cli.codigo != cod_cliente:
                messagebox.showerror("Error", f"El material bibliográfico {material.titulo} está reservado por otro cliente.")
                return False
        
        prestamo :Optional[Prestamo] = None
        for pre in self._prestamos:
            if pre.cliente.codigo == cod_cliente and pre.material.Id == cod_material:
                    prestamo= pre
                    break

        if prestamo is None:
            messagebox.showerror("Error", f"No existe un prestamo del cliente con ID {cod_cliente} con el material bibliografico {material.titulo}.")
            return False       

        nueva_fecha= prestamo.get_fecha_entrega() + timedelta(days=7)
        prestamo.renovar_prestamo(nueva_fecha)

        material.marcar_no_disponible()

        messagebox.showinfo("Renovación exitosa", f"Prestamo con ID: {prestamo.Id} renovado. Nueva fecha de entrega: {nueva_fecha}.")
        return True


    def devolver_material(self, cod_cliente: int, cod_material: int) -> bool:
        """
        Registra la devolución de un material.

        Args:
            cod_cliente: Código del cliente.
            cod_material: ID del material.

        Returns:
            True si la devolución fue exitosa, False en caso contrario.
        """
        cliente: Optional[Cliente] = None
        for cli in self._clientes:
            if cli.codigo == cod_cliente:
                cliente= cli
                break

        if cliente is None:
            messagebox.showerror("Error", f"No existe cliente con ID {cod_cliente}.")
            return False

        material: Optional[Material_Bibliografico] = None
        for mat in self._materiales:
            if mat.Id == cod_material:
                material= mat
                break
        
        if material is None:
            messagebox.showerror("Error", f"No existe material bibliografico con ID {cod_material}.")
            return False

        prestamo: Optional[Prestamo] = None
        for pre in self._prestamos:
            if pre.cliente.codigo == cod_cliente and pre.material.Id == cod_material:
                    prestamo= pre
                    break

        if prestamo is None:
            messagebox.showerror("Error", f"No existe un prestamo del cliente {cod_cliente} con el material bibliografico {cod_material}.")
            return False

        fecha_devolucion= date.today()
        if fecha_devolucion > prestamo.get_fecha_entrega():
            cliente.marcar_vetado()
            dias = (fecha_devolucion - prestamo.get_fecha_entrega()).days
            self.registrar_sancion(cod_cliente, "Retraso en la devolución", prestamo.get_fecha_entrega())
            messagebox.showwarning("Devolución", f"Devolución con retraso de {dias} día(s). Cliente {cliente.nombre} ha sido vetado.")
        else:
            messagebox.showinfo("Devolución", f"Devolución realizada a tiempo. ¡Gracias {cliente.nombre}!")

        material.marcar_disponible()

        self._prestamos.remove(prestamo)

        messagebox.showinfo("Devolución", f"Devolución realizada con éxito.\nPréstamo ID: {prestamo.Id}, Cliente: {cliente.nombre}, Material bibliografico: {material.titulo}.")
        return True
   

    def reservar_material(self, cod_cliente: int, cod_material: int) -> bool:
        """
        Crea una reserva de material.

        Args:
            cod_cliente: Código del cliente.
            cod_material: ID del material.

        Returns:
            True si la reserva fue exitosa, False en caso contrario.
        """
        cliente: Optional[Cliente] = None
        for cli in self._clientes:
            if cli.codigo == cod_cliente:
                cliente= cli
                break
        
        if cliente is None: 
            messagebox.showerror("Error", f"No existe un cliete con ID {cod_cliente}.")
            return False

        if cliente.es_vetado():
            messagebox.showerror("Error", f"El cliente {cliente.nombre} está vetado.")
            return False
        
        material: Optional[Material_Bibliografico] = None
        for mat in self._materiales:
            if mat.Id == cod_material:
                material= mat
                break

        if material is None:
            messagebox.showerror("Error", f"No existe material bibliografico con ID {cod_material}.")
            return False

        if material.get_estado() != "disponible":
            messagebox.showerror("Error", f"El material bibliografico con ID {cod_material} NO se puede reservar porque está prestado.")
            return False

        for res in self._reservas:
            if res.mat.Id == cod_material and res.get_estado() == "activa":
                messagebox.showerror("Error", f"El material bibliografico con ID {cod_material} ya está reservado por el cliente {res.cli.nombre}.")
                return False

        self._contador_reservas += 1
        nueva_reserva = Reserva(self._contador_reservas, cliente, material, date.today(), "activa")

        self._reservas.append(nueva_reserva)

        messagebox.showinfo("Éxito", f"El material bibliografico {material.titulo} ha sido reservado exitosamente por el cliente: {cliente.nombre}.")
        return True
    

    def cancelar_reserva(self, cod_cliente: int, cod_material: int) -> bool:
        """
        Cancela una reserva de material.

        Args:
            cod_cliente: Código del cliente.
            cod_material: ID del material.

        Returns:
            True si la cancelación fue exitosa, False en caso contrario.
        """
        cliente: Optional[Cliente] = None
        for cli in self._clientes:
            if cli.codigo == cod_cliente:
                cliente= cli
                break

        if cliente is None:
            messagebox.showerror("Error", f"No existe un cliente con ID {cod_cliente}.")
            return False

        material: Optional[Material_Bibliografico] = None
        for mat in self._materiales:
            if mat.Id == cod_material:
                material= mat
                break
        
        if material is None:
            messagebox.showerror("Error", f"No existe material bibliografico con ID {cod_material}.")
            return False

        reserva: Optional[Reserva] = None
        for res in self._reservas:
            if res.mat.Id == cod_material and res.cli.codigo == cod_cliente:
                reserva= res
                break

        if reserva is None:
            messagebox.showerror("Error", f"No existe reserva del material {material.titulo} realizada por el cliente {cliente.nombre}.")
            return False

        self._reservas.remove(reserva)

        messagebox.showinfo("Reserva cancelada", f"La reserva del material {material.titulo} ha sido cancelada por el cliente {cliente.nombre}.")
        return True


    def registrar_sancion(self, cod_cliente: int, motivo: str, fecha_entrega: date) -> None:
        """
        Registra una sanción automática por retraso.

        Args:
            cod_cliente: Código del cliente sancionado.
            motivo: Motivo de la sanción.
            fecha_entrega: Fecha límite de entrega incumplida.
        """
        cliente: Optional[Cliente] = None
        for cli in self._clientes:
            if cli.codigo == cod_cliente:
                cliente= cli
                break
        
        if cliente is None:
            messagebox.showerror("Error", f"No existe un cliente con código {cod_cliente}.")
            return False
        
        self._contador_sanciones += 1
        fecha_sancion= date.today()

        dias_retraso= (fecha_sancion - fecha_entrega).days
        if dias_retraso < 1:
            dias_retraso= 1

        monto= dias_retraso * 1000

        sancion= Sancion(self._contador_sanciones, cliente, motivo, fecha_sancion, monto)
        self._sanciones.append(sancion)

        messagebox.showwarning("Sanción registrada", f"Sanción ID {self._contador_sanciones} registrada al cliente {cliente.nombre}, Motivo: {motivo}, Fecha: {fecha_sancion}, Días de retraso: {dias_retraso}, Monto: ${monto}")


    def clientes_vetados(self) -> None:
        """
        Muestra los clientes que se encuentran vetados.
        """
        vetados = []
        for cli in self._clientes:
            if cli.es_vetado():
                vetados.append(cli)

        if not vetados:
            messagebox.showinfo("Clientes vetados", "No hay clientes vetados.")
            return 
        
        lista = "\n".join(str(cli) for cli in vetados) 
        messagebox.showinfo("Lista de Clientes vetados", lista)


    def levantar_sancion(self, id_sancion: int) -> bool:
        """
        Levanta una sanción existente.

        Args:
            id_sancion: ID de la sanción.

        Returns:
            True si la sanción fue eliminada, False en caso contrario.
        """
        sancion: Optional[Sancion] = None
        for san in self._sanciones:
            if san.id_sancion == id_sancion:
                sancion= san
                break

        if sancion is None:
            messagebox.showerror("Error", f"No existe sanción con ID {id_sancion}.")
            return False
        
        cliente= sancion.cliente
        if not cliente.es_vetado():
            messagebox.showinfo("Levantar sanción", f"El cliente {cliente.nombre} no está vetado actualmente.")
            return False
        
        cliente.quitar_vetado()

        self._sanciones.remove(sancion)

        messagebox.showinfo("Levantar sanción", f"Sancion con ID {id_sancion} elimianda. El cliente {cliente.nombre} ya no está vetado.")
        return True


    def eliminar_material(self, codigo: int) -> bool:
        """
        Elimina un material de la biblioteca.

        Args:
            codigo: ID del material.

        Returns:
            True si el material fue eliminado, False en caso contrario.
        """
        material= None

        for mat in self._materiales:
            if mat.Id == codigo:
                material= mat
                break
        
        if material is None:
            messagebox.showerror("Error", f"No existe material bibliográfico con ID {codigo}.")
            return False
        
        if material.get_estado == "prestado":
            messagebox.showerror("Error", f"No se puede eliminar el material bibliográfico {material.titulo} porque está en préstamo.")
            return False
        
        if material.get_estado == "reservado":
            messagebox.showerror("Error", f"No se puede eliminar el material bibliográfico {material.titulo} porque está reservado.")
            return False

        self._materiales.remove(material)

        messagebox.showinfo("Eliminar material", f"El material {codigo} - {material.titulo} ha sido eliminado con éxito.")
        return True
    

    def eliminar_cliente(self, codigo: int) -> bool:
        """
        Elimina un cliente de la biblioteca.

        Args:
            codigo: Código del cliente.

        Returns:
            True si el cliente fue eliminado, False en caso contrario.
        """
        cliente= None

        for cli in self._clientes:
            if cli.codigo == codigo:
                cliente= cli
                break
        
        if cliente is None:
            messagebox.showerror("Error", f"No existe cliente con código {codigo}.")
            return False
        
        for prestamo in self._prestamos:
            if prestamo.cliente.codigo == codigo:
                messagebox.showerror("Error", f"No se puede eliminar al cliente {cliente.nombre} tiene préstamos activos.")
                return False
        
        for reserva in self._reservas:
            if reserva.cli.codigo == codigo:
                messagebox.showerror("Error", f"No se puede eliminar al cliente {cliente.nombre} porque tiene reservas activas.")
                return False

        self._clientes.remove(cliente)

        messagebox.showinfo("Eliminar cliente", f"El cliente {cliente.nombre} ha sido eliminado con éxito.")
        return True


    def ingresar_solo_letras(self, text1: str, text2: str) -> str:
        """
        Solicita una entrada de texto que solo contenga letras.

        Args:
            text1: Título de la ventana de diálogo.
            text2: Mensaje de la ventana de diálogo.

        Returns:
            Cadena de texto válida ingresada por el usuario.
        """
        while True: 
            valor= simpledialog.askstring(text1, text2)

            if valor is None: 
                return None
            
            valor= valor.strip()  

            if not valor: 
                messagebox.showerror("Error", "El campo no puede estar vacio. Intente de nuevo.")
                continue
            
            if all(palabra.isalpha() for palabra in valor.split()):
                return valor  
            
            messagebox.showerror("Error", "Solo se permiten letras. Intente de nuevo.")