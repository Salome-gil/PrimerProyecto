import tkinter as tk
from tkinter import simpledialog, messagebox
from Biblioteca import Biblioteca
from Cliente import Estudiante, Profesor, Empleado
from Material_Bibliografico import Material_Bibliografico

bib = Biblioteca()
def menu_principal():
    root = tk.Tk()
    root.withdraw()  
    
    opcion = -1
    messagebox.showinfo("Bienvenido", "Bienvenido al Menu de la Biblioteca ITM \n Seleccione la opcion que desea")
    
    
    while opcion != 0:
        menu = (
            "--- MENU PRINCIPAL ---\n"
            "1. Gestión de clientes\n"
            "2. Gestión de Material bibliográfico\n"
            "3. Gestión de Préstamos\n"
            "0. Salir\n"
        )
        resp = simpledialog.askinteger("Menú Principal", menu)
        if resp is None: 
            break
        
        try:
            opcion= int(resp)
            match opcion:
                case 0: 
                    messagebox.showinfo("Salir", "Hasta luego")
                case 1: 
                    menu_clientes()
                case 2: 
                    ##menu_materiales()
                #case 3: # Menú de prestamos
                  ##  menu_prestamos()
                #case _: # Opcion invalida
                    messagebox.showerror("Error", "Opción no válida")

        except ValueError :
                messagebox.showwarning("Error", "Opción no válida")


def menu_clientes():

    opcion = -1

    while opcion != 0:
        menu = (
            "--- CLIENTES ---\n"
            "1. Agregar cliente\n"
            "2. Ver clientes\n"
            "3. Buscar cliente\n"
            "4. Informe de clientes vetados\n"
            "0. Volver al menú principal\n"
        )
        resp = simpledialog.askinteger("Clientes", menu)
        if resp is None:  
            break
        
        try:
            opcion= int(resp)
            match opcion:
                case 0:
                    messagebox.showinfo("Salir", "Vuelves al menú principal")

                case 1:
                    op2= -1
                    
                    while op2 != 0:
                        menu2= ("Tipo de cliente\n"
                                "1. Estudiante\n"
                                "2. Profesor\n"
                                "3. Empleado\n"
                                "0. Volver al menú de clientes\n")
                        resp2= simpledialog.askinteger("Tipo de cliente", menu2)
                        if resp is None:
                            break
                        try:
                            op2= int(resp2)
                            match op2:
                                case 0:
                                    messagebox.showinfo("Salir", "Vuelves al menú de clientes")

                                case 1: 
                                    codigo= simpledialog.askinteger("Código", "Código del estudiante: ")
                                    if codigo is None:   
                                        messagebox.showwarning("Advertencia", "Debe ingresar un número de código válido")
                                        break
                                    nombre= bib.ingresar_solo_letras("Nombre", "Nombre del estudiante: ")
                                    if nombre is None:
                                        break
                                    carrera= bib.ingresar_solo_letras("Carrera", "Ingrese la carrera del estudiante: ")
                                    if carrera is None:
                                        break
                                    cliente = Estudiante(codigo, nombre, carrera, False)
                                    bib.agregar_cliente(cliente)

                                case 2: 
                                    codigo= simpledialog.askinteger("Código", "Código del profesor: ")
                                    if codigo is None:   
                                        messagebox.showwarning("Advertencia", "Debe ingresar un número de código válido")
                                        break
                                    nombre= bib.ingresar_solo_letras("Nombre", "Nombre del profesor: ")
                                    if nombre is None:
                                        break
                                    facultad= bib.ingresar_solo_letras("Facultad", "Ingrese la facultad del profesor: ")
                                    if facultad is None:
                                        break
                                    cliente = Profesor(codigo, nombre, facultad, False)
                                    bib.agregar_cliente(cliente)

                                case 3: 
                                    codigo= simpledialog.askinteger("Código", "Código del empleado: ")
                                    if codigo is None:   
                                        messagebox.showwarning("Advertencia", "Debe ingresar un número de código válido")
                                        break
                                    nombre= bib.ingresar_solo_letras("Nombre", "Nombre del empleado: ")
                                    if nombre is None:
                                        break
                                    cargo= bib.ingresar_solo_letras("Cargo", "Ingrese el cargo del empleado: ")
                                    if cargo is None:
                                        break
                                    cliente = Empleado(codigo, nombre, cargo, False)
                                    bib.agregar_cliente(cliente)
                                
                                case _:
                                    messagebox.showerror("Error", "Opción no válida")
                        except ValueError :
                            messagebox.showwarning("Error", "Opción no válida")

                case 2: 
                    bib.ver_clientes()

                case 3:
                    codigo_cli= simpledialog.askinteger("Código", "Ingrese el código del cliente a buscar: ")
                    if codigo_cli is None:
                        messagebox.showwarning("ADVERTENCIA", "Debe de ingresar un código")
                    else:
                        bib.buscar_cliente(codigo_cli)

                case 4: 
                    bib.clientes_vetados()

                case _: 
                    messagebox.showerror("Error", "Opción no válida")

        except ValueError :
                messagebox.showwarning("Error", "Opción no válida")
        
