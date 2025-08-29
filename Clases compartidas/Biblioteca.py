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