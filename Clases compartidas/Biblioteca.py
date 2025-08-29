from typing import List
from Cliente import Cliente 
from Material_Bibliografico import Material_Bibliografico
from Prestamo import Prestamo
from tkinter import messagebox

class Biblioteca:

    def __init__(self) -> None:
        self._clientes: List[Cliente] = []
        self._materiales: List[Material_Bibliografico] = []
        self._prestamos: List[Prestamo] = []

#------------------------------------------------------------------------------------------
#  AGREGAR DATOS
# -----------------------------------------------------------------------------------------    

    def agregar_cliente(self, cliente: Cliente) -> None:    
        self._clientes.append(cliente)
        messagebox.showinfo("Exito", f"Cliente {cliente.get_nombre()} agregado correctamente.")
    
    def agregar_material(self, material: Material_Bibliografico) -> None:
        self._materiales.append(material)
        messagebox.showinfo("Exito", f"Material {material.get_Id()} agregado correctamente.")

#------------------------------------------------------------------------------------------
# BUSCAR DATOS
# -----------------------------------------------------------------------------------------     

    def buscar_cliente(self, buscar_cod: int) -> None:
        for cli in self._clientes:  
            if cli.get_codigo() == buscar_cod:  
                messagebox.showinfo("Exito", f"Cliente encontrado:\n{cli}.")
                return    
    
    def buscar_material(self, buscar_cod: int) -> None:
        for mat in self._materiales:  
            if mat.get_Id() == buscar_cod:  
                messagebox.showinfo("Exito", f"Material bibliografico encontrado:\n{mat}.")
                return  
        
    def buscar_prestamo(self, buscar_cod: int) -> None:
        for pre in self._prestamos:  
            if pre.get_id() == buscar_cod:  
                messagebox.showinfo("Exito", f"Prestamo encontrado:\n{pre}.")
                return  
        

