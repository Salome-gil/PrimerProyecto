"""
Módulo principal de la aplicación de Biblioteca.

Este archivo implementa la interfaz principal basada en menús
para la gestión de clientes, materiales bibliográficos, reservas,
préstamos y sanciones dentro de una biblioteca. Utiliza Tkinter
para mostrar menús interactivos y cuadros de diálogo que permiten
al usuario realizar operaciones de manera sencilla.

Clases y entidades relacionadas:
- Biblioteca: Clase central que administra clientes, materiales, reservas,
  préstamos y sanciones.
- Cliente: Representa a los usuarios de la biblioteca (estudiantes, profesores,
  empleados).
- Material_Bibliografico: Define los recursos disponibles en la biblioteca
  (libros, revistas, etc.).
- Categoria: Permite clasificar los materiales bibliográficos.
- Sede: Representa las diferentes sedes físicas de la biblioteca.

Funcionalidades principales:
- Elección de sede: El usuario selecciona una sede de la biblioteca para operar.
- Menú principal: Desde aquí se accede a las secciones de clientes, materiales,
  reservas, préstamos y sanciones.
- Submenús: Cada sección cuenta con sus propias opciones para agregar, buscar,
  eliminar o listar información según corresponda.
- Validaciones: Se incluyen controles básicos de entrada de datos mediante
  cuadros de diálogo, así como mensajes de advertencia y error.

Uso:
- Ejecutar este archivo como script principal.
- Seleccionar una sede de la biblioteca.
- Navegar a través de los menús y realizar operaciones.
- Finalizar el programa seleccionando la opción "0. Salir".
"""


import tkinter as tk
from tkinter import simpledialog, messagebox
from Biblioteca import Biblioteca
from Cliente import Cliente
from Material_Bibliografico import Material_Bibliografico
from Categoria import Categoria
from Sede import Sede

bib = Biblioteca("Biblioteca Central")

sedes = [
    Sede(1, "Fraternidad", "Calle 10"),
    Sede(2, "Robledo", "Carrera 45"),
    Sede(3, "Castilla", "Avenida 10"),
    Sede(4, "Floresta", "Diagonal 55")
]

for sede in sedes:
    sede.biblioteca = Biblioteca(f"{sede.nombre}")

def eleccion_sede():

    menu = (
        "--- SELECCIÓN DE SEDE ---\n"
        "1. Fraternidad - Calle 10\n"
        "2. Robledo - Carrera 45\n"
        "3. Castilla - Avenida 10\n"
        "4. Floresta - Diagonal 55\n"
        "0. Salir\n"
    )

    resp = simpledialog.askinteger("Elegir sede", menu)
    if resp is None:
        messagebox.showinfo("Salir", "No seleccionaste ninguna sede")
        return None

    if resp == 0:
        messagebox.showinfo("Salir", "Hasta luego")
        return None

    for sede in sedes:
        if sede.id == resp:
            return sede

    messagebox.showerror("Error", "Sede no válida")
    return None


def menu_principal(bib: Biblioteca):

    opcion = -1
    
    while opcion != 0:
        menu = (
            "--- MENU PRINCIPAL ---\n"
            "1. Gestión de clientes\n"
            "2. Gestión de Material bibliográfico\n"
            "3. Gestión de Reservas\n"
            "4. Gestión de Préstamos\n"
            "5. Gestión de Sanciones\n"
            "0. Volver a elección de Sede\n"
        )
        resp = simpledialog.askinteger("Menú Principal", menu)
        if resp is None: 
            break
        
        opcion= int(resp)
        match opcion:
            case 0: 
                return
            case 1: 
                menu_clientes(bib)
            case 2: 
                menu_materiales(bib)
            case 3: 
                menu_reservas(bib)
            case 4: 
                menu_prestamos(bib)
            case 5: 
                menu_sanciones(bib)
            case _: 
                messagebox.showerror("Error", "Opción no válida")


def menu_clientes(bib: Biblioteca):

    opcion = -1

    while opcion != 0:
        menu = (
            "--- CLIENTES ---\n"
            "1. Agregar cliente\n"
            "2. Ver clientes\n"
            "3. Buscar cliente\n"
            "4. Ver clientes vetados\n"
            "5. Eliminar cliente\n"
            "0. Volver al menú principal\n"
        )
        resp = simpledialog.askinteger("Clientes", menu)
        if resp is None: 
            break

        opcion= int(resp)
        match opcion:
            case 0: 
                messagebox.showinfo("Salir", "Vuelves al menú principal")

            case 1: 
                cod= simpledialog.askinteger("Código", "Ingrese el ID del cliente: ")
                if cod is None:
                    continue
                nombre= bib.ingresar_solo_letras("Nombre", "Ingresa el nombre del cliente: ")
                if nombre is None:
                    continue
                
                menu2 = (
                    "--- TIPO DE CLIENTES ---\n"
                    "1. Estudiante\n"
                    "2. Profesor\n"
                    "3. Empleado\n"
                )
                resp2 = simpledialog.askinteger("Clientes", menu2)
                if resp2 is None: 
                    continue
                    
                match resp2:
                    case 1:
                        carrera= bib.ingresar_solo_letras("Carrera", "Ingrese la carrera a la que pertenece: ")
                        if carrera is None:
                            continue
                        cliente = Cliente(cod, nombre, "Estudiante", carrera, False)
                        bib.agregar_cliente(cliente)
                        
                    case 2:
                        facultad= bib.ingresar_solo_letras("Facultad", "Ingrese la facultad a la que pertenece: ")
                        if facultad is None:
                            continue
                        cliente = Cliente(cod, nombre, "Profesor", facultad, False)
                        bib.agregar_cliente(cliente)

                    case 3:
                        cargo= bib.ingresar_solo_letras("Cargo", "Ingrese el cargo al que pertenece: ")
                        if cargo is None:
                            continue
                        cliente = Cliente(cod, nombre, "Empleado", cargo, False)
                        bib.agregar_cliente(cliente)

                    case _: 
                        messagebox.showerror("Error", "Opción no válida")

            case 2: 
                bib.ver_clientes()

            case 3:
                buscar_cod= simpledialog.askinteger("ID", "Ingrese el ID del cliente a buscar: ")
                if buscar_cod is None:
                    messagebox.showwarning("ADVERTENCIA", "Debe de ingresar un ID")
                else:
                    bib.buscar_cliente(buscar_cod)

            case 4: 
                bib.clientes_vetados()

            case 5: 
                cod= simpledialog.askinteger("ID", "Ingrese el ID del cliente a eliminar: ")
                if cod is None:
                    messagebox.showwarning("ADVERTENCIA", "Debe de ingresar un ID")
                else:
                    bib.eliminar_cliente(cod)

            case _: 
                messagebox.showerror("Error", "Opción no válida")
        

def menu_materiales(bib: Biblioteca):
    opcion = -1

    while opcion != 0:
        menu = (
            "--- MATERIALES BIBLIOGRÁFICOS ---\n"
            "1. Agregar material bibliográfico\n"
            "2. Ver materiales bibliográficos\n"
            "3. Buscar material bibliográfico\n"
            "4. Eliminar material bibliográfico\n"
            "5. Agregar categoría\n"
            "6. Ver categorías\n"
            "0. Volver al menú principal\n"
        )
        resp = simpledialog.askinteger("Material Bibliográfico", menu)
        if resp is None: 
            break

        opcion= int(resp)
        match opcion:
            case 0: 
                messagebox.showinfo("Salir", "Vuelves al menú principal")

            case 1: 
                if not bib._categorias:
                    messagebox.showwarning("Categorías", "No hay categorías registradas.\nDebe agregar una categoría primero.")
                    continue
                else:
                    codigo= simpledialog.askinteger("ID", "Ingrese el ID del material bibliografico: ")
                    titulo= bib.ingresar_solo_letras("Titulo", "Ingrese titulo del material bibliográfico: ")
                    if titulo is None:
                        continue
                    autor= bib.ingresar_solo_letras("Autor", "Ingrese autor del material bibliográfico: ")
                    if autor is None:
                        continue
                    categoria = simpledialog.askinteger("Categoría", "Ingrese el ID de la categoría:")
                    if categoria is None:
                        continue

                    categoria_obj= None
                    for cat in bib._categorias:
                        if cat.id_categoria == categoria:
                            categoria_obj= cat
                            break

                    if categoria_obj is None:
                        messagebox.showerror("Error", f"No existe categoría con ID {categoria}.")
                        continue

                material= Material_Bibliografico(codigo, titulo, autor, categoria_obj, sede_actual, "disponible")
                bib.agregar_material(material)

            case 2: 
                bib.ver_materiales()

            case 3: 
                buscar_cod= simpledialog.askinteger("ID", "Ingrese el ID del material bibliografico a buscar: ")
                if buscar_cod is None:
                    messagebox.showwarning("ADVERTENCIA", "Debe de ingresar un ID")
                else:
                    bib.buscar_material(buscar_cod)

            case 4: 
                cod= simpledialog.askinteger("ID", "Ingrese el ID del material bibliografico a eliminar: ")
                if cod is None:
                    messagebox.showwarning("ADVERTENCIA", "Debe de ingresar un ID")
                else:
                    bib.eliminar_material(cod)

            case 5: 
                codigo= simpledialog.askinteger("ID", "Ingrese el ID de la categoría: ")
                nombre= bib.ingresar_solo_letras("Nombre", "Ingrese nombre de la categoría: ")
                if nombre is None:
                    continue
                descripcion= bib.ingresar_solo_letras("Descripción", "Ingrese descripción corta de la categoría: ")
                if descripcion is None:
                    continue

                categoria= Categoria(codigo, nombre, descripcion)
                bib.agregar_categoria(categoria)

            case 6: 
                bib.ver_categorias()

            case _: 
                messagebox.showerror("Error", "Opción no válida")


def menu_prestamos(bib: Biblioteca):
    opcion = -1

    while opcion != 0:
        menu = (
            "--- PRÉSTAMOS ---\n"
            "1. Prestar material\n"
            "2. Ver préstamos\n"
            "3. Buscar préstamo\n"
            "4. Renovar préstamo\n"
            "5. Devolver material\n"
            "0. Volver al menú principal\n"
        )
        resp = simpledialog.askinteger("Préstamos", menu)
        if resp is None: 
            break

        opcion= int(resp)
        match opcion:
            case 0: 
                messagebox.showinfo("Salir", "Vuelves al menú principal")

            case 1:
                cod_cli= simpledialog.askinteger("Código Cliente", "Ingrese el código del cliente para el prestamo: ")
                if cod_cli is None:
                    continue
                cod_mat= simpledialog.askinteger("ID Material", "Ingrese el ID del material bibliográfico para el prestamo: ")
                if cod_mat is None:
                    continue
                resp= bib.prestar_material(cod_cli, cod_mat)

                if not resp:
                    messagebox.showerror("Error", "No se pudo realizar la operación.")

            case 2: 
                bib.ver_prestamos()

            case 3:
                buscar_cod= simpledialog.askinteger("ID", "Ingrese el ID del préstamo a buscar: ")
                if buscar_cod is None:
                    continue
                bib.buscar_prestamo(buscar_cod)

            case 4: 
                cod_cli= simpledialog.askinteger("Código Cliente", "Ingrese el código del cliente para renovar el prestamo: ")
                if cod_cli is None:
                    continue
                cod_mat= simpledialog.askinteger("ID Material", "Ingrese el ID del material bibliográfico para renovar el prestamo: ")
                if cod_mat is None:
                    continue
                resp= bib.renovar_prestamo(cod_cli, cod_mat)

                if not resp:
                    messagebox.showerror("Error", "No se pudo realizar la operación.")

            case 5: 
                cod_cli= simpledialog.askinteger("Código Cliente", "Ingrese el código del cliente para devolver el prestamo: ")
                if cod_cli is None:
                    continue
                cod_mat= simpledialog.askinteger("ID Material", "Ingrese el ID del material bibliográfico para devolver el prestamo: ")
                if cod_mat is None:
                    continue
                resp= bib.devolver_material(cod_cli, cod_mat)

                if not resp:
                    messagebox.showerror("Error", "No se pudo realizar la operación.")

            case _: 
                messagebox.showerror("Error", "Opción no válida")


def menu_reservas(bib: Biblioteca):
    opcion = -1

    while opcion != 0:
        menu = (
            "--- RESERVAS  ---\n"
            "1. Ver reservas\n"
            "2. Reservar material bibliográfico\n"
            "3. Cancelar reserva\n"
            "4. Buscar reserva\n"
            "0. Volver al menú principal\n"
        )
        resp = simpledialog.askinteger("Reservas", menu)
        if resp is None: 
            break

        opcion= int(resp)
        match opcion:
            case 0: 
                messagebox.showinfo("Salir", "Vuelves al menú principal")

            case 1: 
                bib.ver_reservas()

            case 2: 
                cod_cli= simpledialog.askinteger("Código Cliente", "Ingrese el código del cliente para la reserva: ")
                if cod_cli is None:
                    continue
                cod_mat= simpledialog.askinteger("ID Material", "Ingrese el ID del material bibliográfico para la reserva: ")
                if cod_mat is None:
                    continue
                resp= bib.reservar_material(cod_cli, cod_mat)

                if not resp:
                    messagebox.showerror("Error", "No se pudo realizar la operación.")

            case 3: 
                cod_cli= simpledialog.askinteger("Código Cliente", "Ingrese el código del cliente para cancelar la reserva: ")
                if cod_cli is None:
                    continue
                cod_mat= simpledialog.askinteger("ID Material", "Ingrese el ID del material bibliográfico para cancelar la reserva: ")
                if cod_mat is None:
                    continue
                resp= bib.cancelar_reserva(cod_cli, cod_mat)

                if not resp:
                    messagebox.showerror("Error", "No se pudo realizar la operación.")

            case 4: 
                buscar_cod= simpledialog.askinteger("ID", "Ingrese el ID de la reserva a buscar: ")
                if buscar_cod is None:
                    messagebox.showwarning("ADVERTENCIA", "Debe de ingresar un ID")
                else:
                    bib.buscar_reserva(buscar_cod)

            case _: 
                messagebox.showerror("Error", "Opción no válida")


def menu_sanciones(bib: Biblioteca):
    opcion = -1

    while opcion != 0:
        menu = (
            "--- SANCIONES ---\n"
            "1. Ver sanciones activas\n"
            "2. Crear sanción\n"
            "3. Levantar sanción\n"
            "4. Buscar sanción\n"
            "0. Volver al menú principal\n"
        )
        resp = simpledialog.askinteger("Sanciones", menu)
        if resp is None: 
            break

        opcion= int(resp)
        match opcion:
            case 0: 
                messagebox.showinfo("Salir", "Vuelves al menú principal")

            case 1: 
                bib.ver_sanciones()
                
            case 2: 
                cliente= simpledialog.askinteger("Cliente", "Ingrese el ID del cliente a sancionar: ")
                if cliente is None:
                    continue

                cli_obj= None
                for cli in bib._clientes:
                    if cli.codigo == cliente:
                        cli_obj= cli
                        break

                if cli_obj is None:
                    messagebox.showerror("Error", f"No existe cliente con ID {cliente}.")
                    continue

                motivo= bib.ingresar_solo_letras("Motivo", "Ingrese el motivo de la sanción: ")
                if motivo is None:
                    continue

                monto= simpledialog.askfloat("Monto", "Ingrese el valor de la sanción: ")
                if monto is None:
                    continue

                bib.agregar_sancion(cli_obj, motivo, monto)

            case 3: 
                id_sancion= simpledialog.askinteger("ID Sanción", "Ingrese el ID de la sanción a levantar: ")
                if id_sancion is None:
                    continue
                resp= bib.levantar_sancion(id_sancion)

                if not resp:
                    messagebox.showerror("Error", "No se pudo realizar la operación.")

            case 4:
                buscar_cod= simpledialog.askinteger("ID", "Ingrese el ID de la sanción a buscar: ")
                if buscar_cod is None:
                    messagebox.showwarning("ADVERTENCIA", "Debe de ingresar un ID")
                else:
                    bib.buscar_sancion(buscar_cod)

            case _: 
                messagebox.showerror("Error", "Opción no válida")


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    messagebox.showinfo("Bienvenido", "Bienvenido al Menu de la Biblioteca ITM")

    while True:
        sede_actual = eleccion_sede()
        if sede_actual is None:  
            break
        menu_principal(sede_actual.biblioteca)
