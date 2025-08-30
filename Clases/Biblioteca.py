from typing import List, Optional
from Cliente import Cliente 
from Material_Bibliografico import Material_Bibliografico
from Prestamo import Prestamo
from datetime import date, timedelta
from tkinter import messagebox, simpledialog

class Biblioteca:

    # Constructor de la clase Biblioteca, inicializa las listas de clientes, materiales y préstamos.
    def __init__(self) -> None:
        self._clientes: List[Cliente] = []
        self._materiales: List[Material_Bibliografico] = []
        self._prestamos: List[Prestamo] = []
        self._contador_prestamos: int = 0 # Contador para asignar ID cuando se crea un préstamo

#------------------------------------------------------------------------------------------
#  AGREGAR DATOS
# -----------------------------------------------------------------------------------------    

    # Agrega un cliente a la biblioteca, validando que no exista previamente.
    def agregar_cliente(self, cliente: Cliente) -> None:
        for cli in self._clientes: # recorre la lista con la variable cli
            if cli.get_codigo() == cliente.get_codigo(): # Verifica si el codigo ya existe
                messagebox.showerror("Error", f"El cliente con código {cliente.get_codigo()} ya existe.")
                return  # Evita que se agregue el duplicado

        # Si no existe, lo agrega a la lista    
        self._clientes.append(cliente)
        messagebox.showinfo("Exito", f"Cliente {cliente.get_nombre()} agregado correctamente.")
    
    # Agrega un material bibliográfico, validando que no exista previamente.
    def agregar_material(self, material: Material_Bibliografico) -> None:
        for mat in self._materiales: # recorre la lista con la variable mat
            if mat.get_Id() == material.get_Id(): # Verifica si el ID ya existe
                messagebox.showerror("Error", f"El material bibliografico con ID {material.get_Id()} ya existe.")
                return  # Evita que se agregue el duplicado
            
        # Si no existe, lo agrega a la lista
        self._materiales.append(material)
        messagebox.showinfo("Exito", f"Material {material.get_Id()} agregado correctamente.")

#------------------------------------------------------------------------------------------
# BUSCAR DATOS
# -----------------------------------------------------------------------------------------     

    # Busca un cliente por su código.
    def buscar_cliente(self, buscar_cod: int) -> None:
        for cli in self._clientes:  # Recorre la lista de clientes
            if cli.get_codigo() == buscar_cod:  # Compara el código buscado con cada cliente
                messagebox.showinfo("Exito", f"Cliente encontrado:\n{cli}.")
                return   # Termina el método si encuentra el cliente
        # Si terminó el ciclo sin encontrar, muestra mensaje de error
        messagebox.showerror("Error", f"No se encontró un cliente con ID {buscar_cod}.")    
    
    # Busca un material bibliográfico por su ID.
    def buscar_material(self, buscar_cod: int) -> None:
        for mat in self._materiales:  # Recorre la lista de materiales
            if mat.get_Id() == buscar_cod:  # Compara el código buscado con cada material
                messagebox.showinfo("Exito", f"Material bibliografico encontrado:\n{mat}.")
                return  # Termina el método si encuentra el material
        # Si terminó el ciclo sin encontrar, muestra mensaje de error
        messagebox.showerror("Error",f"No se encontró material bibliografico con ID {buscar_cod}.")

    # Busca un préstamo por su ID.
    def buscar_prestamo(self, buscar_cod: int) -> None:
        for pre in self._prestamos:  # Recorre la lista de préstamos
            if pre.get_id() == buscar_cod:  # Compara el código buscado con cada préstamo
                messagebox.showinfo("Exito", f"Prestamo encontrado:\n{pre}.")
                return  # Termina el método si encuentra el prestamo
        # Si terminó el ciclo sin encontrar, muestra mensaje de error
        messagebox.showerror("Error", f"No se encontró prestamo con ID {buscar_cod}.")
    
#------------------------------------------------------------------------------------------
# VER LISTADO DE DATOS
# -----------------------------------------------------------------------------------------     

    # Muestra la lista de todos los clientes registrados.
    def ver_clientes(self) -> bool:
        if not self._clientes:  # si la lista está vacía
            messagebox.showerror("Error", "No hay clientes registrados.")
            return False
        
        lista = "\n".join(str(cli) for cli in self._clientes) # convierte cada cliente en texto
        messagebox.showinfo("Listado de Clientes", lista) # muestra los clientes
        return True
    
    # Muestra la lista de materiales bibliográficos registrados.
    def ver_materiales(self) -> bool:
        if not self._materiales:  # si la lista está vacía
            messagebox.showerror("Error", "No hay materiales bibliograficos registrados.")
            return False
        
        lista = "\n".join(str(mat) for mat in self._materiales) # convierte cada material en texto
        messagebox.showinfo("Listado de Materiales Bibliograficos", lista) # muestra los materiales
        return True
    
    # Muestra la lista de préstamos registrados.
    def ver_prestamos(self) -> bool:
        if not self._prestamos:  # si la lista está vacía
            messagebox.showerror("Error", "No hay prestamos registrados.")
            return False
        
        lista= "\n".join(str(pre) for pre in self._prestamos) # convierte cada préstamo en texto
        messagebox.showinfo("Listado de Prestamos", lista) # muestra los préstamos
        return True
    
#------------------------------------------------------------------------------------------
# PRESTAR MATERIAL
# -----------------------------------------------------------------------------------------     

    # Crea un préstamo de un material bibliográfico a un cliente específico.
    def prestar_material(self, cod_cliente: int, cod_material: int) -> bool:
        
        #validar que cliente exista
        cliente: Optional[Cliente] = None
        for cli in self._clientes:
            if cli.get_codigo() == cod_cliente:
                cliente= cli
                break

        if cliente is None:
            messagebox.showerror("Error", f"No existe un cliente con código {cod_cliente}.")
            return False
        
        #validar que el cliente no este vetado
        if cliente.es_vetado():
            messagebox.showerror("Error", f"El cliente {cliente.get_nombre()} está vetado.")
            return False

        # validar que el material exista
        material: Optional[Material_Bibliografico] = None
        for mat in self._materiales:
            if mat.get_Id() == cod_material:
                material = mat
                break

        if material is None:
            messagebox.showerror("Error", f"No existe material bibliográfico con código {cod_material}.")
            return False
        
        #validar que el material no este reservado o si esta resrvado que sea el mismo cliente del prestamo
        if material.get_reservado():
            if material.get_cliente_reserva()  != cod_cliente:
                messagebox.showerror("Error", f"El material bibliográfico {material.get_Id()} está reservado por otro cliente.")
                return False
            else:
                # Si es el mismo cliente que lo reservó, se permite el préstamo
                material.cancelar_reserva(cod_cliente)
        
        #validar que el material este disponible 
        if material.get_estado() != "disponible":
            messagebox.showerror("Error", f"El material bibliográfico {material.get_Id()} no está disponible.")
            return False

        # Se crea el ID del préstamo
        self._contador_prestamos += 1
        nuevo_id = self._contador_prestamos

        # Se establecen las fechas del prestamo y entrega 
        fecha_prestamo = date.today()
        fecha_entrega = fecha_prestamo + timedelta(days=7)

        # Se crea el prestamo y se añade a la lista
        prestamo = Prestamo(nuevo_id, cod_cliente, cod_material, fecha_prestamo, fecha_entrega)
        self._prestamos.append(prestamo)

        # Cambiar estado del material
        material.marcar_no_disponible()

        messagebox.showinfo("Préstamo creado con exito", f"Préstamo creado. ID={nuevo_id}, Cliente={cliente.get_nombre()}, Fecha de entrega {fecha_entrega}")
        return True
    
#------------------------------------------------------------------------------------------
# RENOVAR PRESTAMO
# -----------------------------------------------------------------------------------------     

    # Renueva un préstamo existente agregando 7 días a la fecha de entrega.
    def renovar_prestamo(self, cod_cliente: int, cod_material: int) -> bool:

        # Verificar que el cliente exista y no esté vetado
        cliente:Optional[Cliente] = None
        for cli in self._clientes:
            if cli.get_codigo() == cod_cliente:
                cliente= cli
                break

        # Si el cliente no existe 
        if cliente is None:
            messagebox.showerror("Error", f"No existe cliente con ID {cod_cliente}.")
            return False
        
        # Si el cliente está vetado 
        if cliente.es_vetado():
            messagebox.showerror("Error", f"El cliente {cliente.get_nombre()} con ID {cod_cliente} se encuentra vetado.")
            return False

        # Verificar que el material exista y no esté reservado
        material: Optional[Material_Bibliografico] = None
        for mat in self._materiales:
            if mat.get_Id() == cod_material:
                material= mat
                break

        # Si el material no existe 
        if material is None:
            messagebox.showerror("Error", f"No existe material bibliografico con ID {cod_material}.")
            return False
        
        # Si el material esta reservado por un cliente diferente al del prestamo
        if material.get_reservado() and material.get_cliente_reserva() != cod_cliente:
            messagebox.showerror("Error", f"El material {cod_material} está reservado por otro cliente.")
            return False
        
        # Validar que el prestamo exista y que el cliente sea el mismo del material
        prestamo :Optional[Prestamo] = None
        for pre in self._prestamos:
            if pre.get_cod_cliente() == cod_cliente and pre.get_cod_material() == cod_material:
                    prestamo= pre
                    break

        # Si el prestamo no existe    
        if prestamo is None:
            messagebox.showerror("Error", f"No existe un prestamo del cliente con ID {cod_cliente} con el material bibliografico {cod_material}.")
            return False       

        # Cambio de la fecha de la entrega
        nueva_fecha= prestamo.get_fecha_entrega() + timedelta(days=7)
        prestamo.renovar_prestamo(nueva_fecha)

        # Asegurar que el material siga marcado como no disponible
        material.marcar_no_disponible()

        messagebox.showinfo("Renovación exitosa", f"Prestamo con ID: {prestamo.get_id()} renovado. Nueva fecha de entrega: {nueva_fecha}.")
        return True
  
#------------------------------------------------------------------------------------------
# DEVOLVER MATERIAL#
# -----------------------------------------------------------------------------------------     

    # Devuelve un material prestado por un cliente.
    def devolver_material(self, cod_cliente: int, cod_material: int) -> bool:
        
        # Verificar que exista cliente
        cliente: Optional[Cliente] = None
        for cli in self._clientes:
            if cli.get_codigo() == cod_cliente:
                cliente= cli
                break

        # Si el cliente no existe
        if cliente is None:
            messagebox.showerror("Error", f"No existe cliente con ID {cod_cliente}.")
            return False

        # Verificar que exista el material
        material: Optional[Material_Bibliografico] = None
        for mat in self._materiales:
            if mat.get_Id() == cod_material:
                material= mat
                break
        
        # Si el material no existe
        if material is None:
            messagebox.showerror("Error", f"No existe material bibliografico con ID {cod_material}.")
            return False

        # Validar que el prestamo exista y que el cliente sea el mismo del prestamo
        prestamo: Optional[Prestamo] = None
        for pre in self._prestamos:
            if pre.get_cod_cliente() == cod_cliente and pre.get_cod_material() == cod_material:
                    prestamo= pre
                    break

        # Si el prestamo no existe
        if prestamo is None:
            messagebox.showerror("Error", f"No existe un prestamo del cliente con ID {cod_cliente} con el material bibliografico {cod_material}.")
            return False

        # Verificar que la devolución este a tiempo, si no, se marca como vetado
        fecha_devolucion= date.today()
        if fecha_devolucion > prestamo.get_fecha_entrega():
            cliente.marcar_vetado()
            dias = (fecha_devolucion - prestamo.get_fecha_entrega()).days
            messagebox.showwarning("Devolución", f"Devolución con retraso de {dias} día(s). Cliente {cliente.get_nombre()} ha sido vetado.")
        else:
            messagebox.showinfo("Devolución", f"Devolución realizada a tiempo. ¡Gracias {cliente.get_nombre()}!")

        # Cambiar el estado del material
        material.marcar_disponible()

        # Eliminar prestamo de la lista de prestamos
        self._prestamos.remove(prestamo)

        messagebox.showinfo("Devolución", f"Devolución realizada con éxito.\nPréstamo ID: {prestamo.get_id()}, Cliente: {cliente.get_nombre()}, Material bibliografico: {cod_material}.")
        return True
    
#------------------------------------------------------------------------------------------
# RESERVAR MATERIAL
# -----------------------------------------------------------------------------------------     

    # Permite reservar un material bibliográfico para un cliente.
    def reservar_material(self, cod_cliente: int, cod_material: int) -> bool:

        # Validar que el cliente exista
        cliente: Optional[Cliente] = None
        for cli in self._clientes:
            if cli.get_codigo() == cod_cliente:
                cliente= cli
                break
        
        # Si el cliente no existe
        if cliente is None: 
            messagebox.showerror("Error", f"No existe un cliete con ID {cod_cliente}.")
            return False

        # Validar que el cliente no esté vetado
        if cliente.es_vetado():
            messagebox.showerror("Error", f"El cliente {cliente.get_nombre()} está vetado.")
            return False
        
        # Validar que el material exista
        material: Optional[Material_Bibliografico] = None
        for mat in self._materiales:
            if mat.get_Id() == cod_material:
                material= mat
                break

        # Si el material no existe
        if material is None:
            messagebox.showerror("Error", f"No existe material bibliografico con ID {cod_material}.")
            return False

        # Validar que el material este disponible
        if material.get_estado() != "disponible":
            messagebox.showerror("Error", f"El material bibliografico con ID {cod_material} NO se puede reservar porque está prestado.")
            return False

        # Validar que el material no este reservado
        if material.get_reservado():
            messagebox.showerror("Error", f"El material bibliografico con ID {cod_material} ya se encuentra reservado por el cliente {cliente.get_nombre()}.")
            return False

        # Marcar el material como reservado
        material.reservar(cod_cliente)

        messagebox.showinfo("Material reservado con éxito", f"El material bibliografico {cod_material} ha sido reservado exitosamente por el cliente: {cliente.get_nombre()}.")
        return True
    
#------------------------------------------------------------------------------------------
# CANCELAR RESERVA
# -----------------------------------------------------------------------------------------     
    # Cancela la reserva de un material bibliográfico para un cliente específico.
    def cancelar_reserva(self, cod_cliente: int, cod_material: int) -> bool:
        # Validar que el cliente exista
        cliente: Optional[Cliente] = None
        for cli in self._clientes:
            if cli.get_codigo() == cod_cliente:
                cliente= cli
                break
        # Si el cliente no existe
        if cliente is None:
            messagebox.showerror("Error", f"No existe un cliente con ID {cod_cliente}.")
            return False
        # Validar que el material exista
        material: Optional[Material_Bibliografico] = None
        for mat in self._materiales:
            if mat.get_Id() == cod_material:
                material= mat
                break
        # Si el material no existe
        if material is None:
            messagebox.showerror("Error", f"No existe material bibliografico con ID {cod_material}.")
            return False
        # Validar que el material este reservado
        if not material.get_reservado():
            messagebox.showerror("Error", f"El material bibliografico con ID {cod_material} No se encuentra reservado.")
            return False
        # Cancelar la reserva si es el mismo cliente del prestamo, cambiar el estado de "reserva"
        if material.cancelar_reserva(cod_cliente):
            messagebox.showinfo("Reserva cancelada", f"La reserva del material {cod_material} ha sido cancelada por el cliente {cliente.get_nombre()}.")
            return True
        else:
            messagebox.showwarning("Cancelar reserva", f"El material {cod_material} fue reservado por otro cliente.")
            return False

#------------------------------------------------------------------------------------------
# ELIMINAR PRESTAMO
# -----------------------------------------------------------------------------------------     
    # Elimina un préstamo existente y marca el material como disponible nuevamente.
    def eliminar_prestamo(self, cod_prestamo: int) -> None:
        # Validar que el prestamo exista
        prestamo: Optional[Prestamo] = None
        for pre in self._prestamos:
            if pre.get_id() == cod_prestamo:
                prestamo = pre
                break
        # Si el prestamo no existe
        if prestamo is None:
            messagebox.showerror("Error", f"No existe un préstamo con ID {cod_prestamo}.")
        # Buscar el material del prestamo
        material: Optional[Material_Bibliografico] = None
        for mat in self._materiales:
            if  mat.get_Id() == prestamo.get_cod_material():
                material= mat
                break
        # Volver a marcar el material como disponible
        if material is not None:
            material.marcar_disponible()
        # Eliminar el prestamo de la lista
        self._prestamos.remove(prestamo)

        messagebox.showinfo("Prestamo eliminado con éxito", f"Préstamo con ID {cod_prestamo} eliminado correctamente.")
    
#------------------------------------------------------------------------------------------
# INFORME DE CLIENTES VETADOS
# -----------------------------------------------------------------------------------------     

    # Muestra una lista de todos los clientes que se encuentran vetados
    def clientes_vetados(self) -> bool:
        vetados = [cli for cli in self._clientes if cli.es_vetado()]
        if not vetados:
            messagebox.showinfo("Clientes vetados", "No hay clientes vetados.")
            return False
                    # join une todas las cadenas generadas por el bucle en una sola cadena.
        lista = "\n".join(str(cli) for cli in vetados) # Llama al metodo __str__() de la clase cliente
        messagebox.showinfo("Lista de Clientes vetados", lista)
        return True
    
#------------------------------------------------------------------------------------------
# METODOS DE VALIDACIÓN
# -----------------------------------------------------------------------------------------     
    # Solicita al usuario ingresar un texto que contenga únicamente letras.
    def ingresar_solo_letras(self, text1: str, text2: str) -> str:

        while True: # Se repetirá hasta que se cumpla una condición de salida dentro del bucle.
            valor= simpledialog.askstring(text1, text2)
            if valor is None:
                return None
            if all(palabra.isalpha() for palabra in valor.split()): # Se verifica que cada palabra tenga solo letras (sin números ni símbolos).
                return valor.strip()  # elimina espacios al inicio y final de la cadena.
            messagebox.showerror("Error", "Solo se permiten letras. Intente de nuevo.")