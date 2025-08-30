import tkinter as tk
from tkinter import simpledialog, messagebox
from Biblioteca import Biblioteca
from Cliente import Estudiante, Profesor, Empleado
from Material_Bibliografico import Material_Bibliografico

bib = Biblioteca()

#--------------------------------
# MENÚ PRINCIPAL
#--------------------------------
def menu_principal():
    root = tk.Tk()
    root.withdraw()  # ocultamos ventana principal
    
    # Se inicializa opcion y se muestra un mensaje de bienvenida.
    opcion = -1
    messagebox.showinfo("Bienvenido", "Bienvenido al Menu de la Biblioteca ITM \n Seleccione la opcion que desea")
    
    # El bucle mantiene activo el menú principal hasta que el usuario elija salir (opcion == 0).
    while opcion != 0:
        menu = (
            "--- MENU PRINCIPAL ---\n"
            "1. Gestión de clientes\n"
            "2. Gestión de Material bibliográfico\n"
            "3. Gestión de Préstamos\n"
            "0. Salir\n"
        )
        resp = simpledialog.askinteger("Menú Principal", menu)
        if resp is None:  # Si el usuario cancela, el bucle termina.
            break
        
        try:
            opcion= int(resp)
            match opcion:
                case 0: # Opción para salir
                    messagebox.showinfo("Salir", "Hasta luego")
                case 1: # Menú de clientes
                    menu_clientes()
                case 2: # Menú de material
                    menu_materiales()
                case 3: # Menú de prestamos
                    menu_prestamos()
                case _: # Opcion invalida
                    messagebox.showerror("Error", "Opción no válida")

        except ValueError :
                messagebox.showwarning("Error", "Opción no válida")

# ---------------------------
# SUBMENÚ CLIENTES
# ---------------------------
def menu_clientes():

    # Se inicializa opcion 
    opcion = -1

    # El bucle mantiene activo el menú hasta que el usuario elija salir (opcion == 0).
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
        if resp is None:  # Si el usuario cancela, el bucle termina.
            break
        
        try:
            opcion= int(resp)
            match opcion:
                case 0: # Opción para salir
                    messagebox.showinfo("Salir", "Vuelves al menú principal")

                case 1: # Agregar cliente
                    op2= -1
                    # Submenú para seleccionar el tipo de cliente al agregar.
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
                                case 0: # Opción para salir
                                    messagebox.showinfo("Salir", "Vuelves al menú de clientes")

                                case 1: # Pedir datos desde la herencia y se crea un objeto Estudiante.
                                    codigo= simpledialog.askinteger("Código", "Código del estudiante: ")
                                    if codigo is None:   # si cancelan o no ingresan nada
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

                                case 2: # Pedir datos desde la herencia y se crea un objeto Profesor
                                    codigo= simpledialog.askinteger("Código", "Código del profesor: ")
                                    if codigo is None:   # si cancelan o no ingresan nada
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

                                case 3: # Pedir datos desde la herencia y se crea un objeto Empleado
                                    codigo= simpledialog.askinteger("Código", "Código del empleado: ")
                                    if codigo is None:   # si cancelan o no ingresan nada
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

                case 2: # Ver listado de clientes
                    bib.ver_clientes()

                case 3: # Buscar cliente
                    codigo_cli= simpledialog.askinteger("Código", "Ingrese el código del cliente a buscar: ")
                    if codigo_cli is None:
                        messagebox.showwarning("ADVERTENCIA", "Debe de ingresar un código")
                    else:
                        bib.buscar_cliente(codigo_cli)

                case 4: # Informe de clientes vetados
                    bib.clientes_vetados()

                case _: # Opcion invalida
                    messagebox.showerror("Error", "Opción no válida")

        except ValueError :
                messagebox.showwarning("Error", "Opción no válida")
        
# ---------------------------
# SUBMENÚ MATERIALES
# ---------------------------
def menu_materiales():
    # Se inicializa opcion 
    opcion = -1

    # El bucle mantiene activo el menú hasta que el usuario elija salir (opcion == 0).
    while opcion != 0:
        menu = (
            "--- MATERIALES BIBLIOGRÁFICOS ---\n"
            "1. Agregar material\n"
            "2. Ver materiales\n"
            "3. Buscar material\n"
            "4. Reservar material\n"
            "5. Cancelar reserva\n"
            "0. Volver al menú principal\n"
        )
        resp = simpledialog.askinteger("Materiales", menu)
        if resp is None:  # Si el usuario cancela, el bucle termina.
            break

        try:
            opcion= int(resp)
            match opcion:
                case 0: # Opción para salir
                    messagebox.showinfo("Salir", "Vuelves al menú principal")

                case 1: # Agregar material, se inicializa como disponible y sin reserva.
                    codigo= simpledialog.askinteger("ID", "Ingrese el ID del material bibliografico: ")
                    material= Material_Bibliografico(codigo, "disponible", None, False)
                    bib.agregar_material(material)

                case 2: # Ver todos los materiales
                    bib.ver_materiales()

                case 3: # Buscar material
                    buscar_cod= simpledialog.askinteger("ID", "Ingrese el ID del material bibliografico a buscar: ")
                    if buscar_cod is None:
                        messagebox.showwarning("ADVERTENCIA", "Debe de ingresar un ID")
                    else:
                        bib.buscar_material(buscar_cod)

                case 4: # Reservar
                    cod_cliente= simpledialog.askinteger("Código cliente", "Ingrese código del cliente para la reserva: ")
                    cod_material= simpledialog.askinteger("ID material bibliografico", "Ingrese el ID del material bibliografico para reservar: ")
                    resp= bib.reservar_material(cod_cliente, cod_material)

                    if not resp:
                        messagebox.showerror("Error", "No se pudo realizar la reserva.")

                case 5: # Cancelar reserva
                    cod_cliente= simpledialog.askinteger("Código cliente", "Ingrese código del cliente para cancelar la reserva: ")
                    cod_material= simpledialog.askinteger("ID material bibliografico", "Ingrese el ID del material bibliografico para cancelar la reservar: ")
                    resp= bib.cancelar_reserva(cod_cliente, cod_material)

                    if not resp:
                        messagebox.showerror("Error", "No se pudo cancelar la reserva.")

                case _: # Opcion invalida
                    messagebox.showerror("Error", "Opción no válida")

        except ValueError :
                messagebox.showwarning("Error", "Opción no válida")        

# ---------------------------
# SUBMENÚ PRÉSTAMOS
# ---------------------------
def menu_prestamos():
    # Se inicializa opcion 
    opcion = -1

    # El bucle mantiene activo el menú hasta que el usuario elija salir (opcion == 0).
    while opcion != 0:
        menu = (
            "--- PRÉSTAMOS ---\n"
            "1. Prestar material\n"
            "2. Ver préstamos\n"
            "3. Buscar préstamo\n"
            "4. Renovar préstamo\n"
            "5. Devolver material\n"
            "6. Eliminar préstamo\n"
            "0. Volver al menú principal\n"
        )
        resp = simpledialog.askinteger("Préstamos", menu)
        if resp is None:  # Si el usuario cancela, el bucle termina.
            break

        try:
            opcion= int(resp)
            match opcion:
                case 0: # Opción para salir
                    messagebox.showinfo("Salir", "Vuelves al menú principal")

                case 1: # Agregar prestamos
                    cod_cli= simpledialog.askinteger("Código", "Ingrese el código del cliente para el prestamo: ")
                    cod_mat= simpledialog.askinteger("ID", "Ingrese el ID del material bibliografico para el prestamo: ")
                    resp= bib.prestar_material(cod_cli, cod_mat)

                    if not resp:
                        messagebox.showerror("Error", "No se pudo realizar el prestamo.")

                case 2: # Ver prestamos
                    bib.ver_prestamos()

                case 3: # Buscar prestamos
                    cod_prestamo= simpledialog.askinteger("ID", "Ingrese el ID del prestamo a buscar: ")
                    if cod_prestamo is None:
                        messagebox.showwarning("ADVERTENCIA", "Debe de ingresar un código")
                    else:
                        bib.buscar_prestamo(cod_prestamo)

                case 4: # Renovar material
                    cod_cli= simpledialog.askinteger("Código", "Ingrese el código del cliente para renovar el prestamo: ")
                    cod_mat= simpledialog.askinteger("ID", "Ingrese el ID del material bibliografico para renovar el prestamo: ")
                    resp= bib.renovar_prestamo(cod_cli, cod_mat)

                    if not resp:
                        messagebox.showerror("Error", "No se pudo realizar la renovación del prestamo.")

                case 5: # Devolver material
                    cod_cli= simpledialog.askinteger("Código", "Ingrese el código del cliente para devolver el prestamo: ")
                    cod_mat= simpledialog.askinteger("ID", "Ingrese el ID del material bibliografico para devolver el prestamo: ")
                    resp= bib.devolver_material(cod_cli, cod_mat)
                    
                    if not resp:
                        messagebox.showerror("Error", "No se pudo realizar la devolución del prestamo.")

                case 6: # Eliminar prestamo
                    cod_pres= simpledialog.askinteger("ID", "Ingrese el ID del prestamo a eliminar: ")
                    bib.eliminar_prestamo(cod_pres)

                case _: # Opcion invalida
                    messagebox.showerror("Error", "Opción no válida")

        except ValueError :
                messagebox.showwarning("Error", "Opción no válida")       

# ---------------------------
# MAIN
# ---------------------------
if __name__ == "__main__":
    menu_principal()      

