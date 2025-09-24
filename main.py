import tkinter as tk
import getpass
from uuid import UUID
from typing import Optional, cast
from tkinter import simpledialog, messagebox
from sqlalchemy.orm import joinedload
from datetime import date, datetime, timedelta

from auth.security import PasswordManager
from database.config import SessionLocal, create_tables

from crud.Biblioteca_crud import BibliotecaCRUD
from crud.Categoria_crud import CategoriaCRUD
from crud.Cliente_crud import ClienteCRUD
from crud.Material_Bibliografico_crud import MaterialBibliograficoCRUD
from crud.Prestamo_crud import PrestamoCRUD
from crud.Reserva_crud import ReservaCrud
from crud.Sancion_crud import SancionCRUD
from crud.Sede_crud import SedeCRUD
from crud.Usuario_crud import UsuarioCRUD

from entities.Biblioteca import Biblioteca
from entities.Categoria import Categoria
from entities.Cliente import Cliente
from entities.Material_Bibliografico import Material_Bibliografico
from entities.Prestamo import Prestamo
from entities.Reserva import Reserva
from entities.Sancion import Sancion
from entities.Sede import Sede
from entities.Usuario import Usuario

class SistemaGestion:

    def __init__(self):
        """
        Inicializa el sistema de gestión bibliotecaria.

        Atributos:
            db (SessionLocal): Sesión activa de la base de datos.
            usuario_crud (UsuarioCRUD): CRUD para gestión de usuarios.
            sede_crud (SedeCRUD): CRUD para gestión de sedes.
            biblioteca_crud (BibliotecaCRUD): CRUD para gestión de bibliotecas.
            categoria_crud (CategoriaCRUD): CRUD para gestión de categorías.
            cliente_crud (ClienteCRUD): CRUD para gestión de clientes.
            material_crud (MaterialBibliograficoCRUD): CRUD para gestión de materiales bibliográficos.
            prestamo_crud (PrestamoCRUD): CRUD para gestión de préstamos.
            reserva_crud (ReservaCrud): CRUD para gestión de reservas.
            sancion_crud (SancionCRUD): CRUD para gestión de sanciones.
            usuario_actual (Optional[Usuario]): Usuario actualmente autenticado.
            sede_actual (Optional[Sede]): Sede actualmente activa.
        """
        self.db = SessionLocal()
        self.crear_admin_si_no_existe()
        self.usuario_crud = UsuarioCRUD(self.db)
        self.sede_crud= SedeCRUD(self.db)
        self.biblioteca_crud= BibliotecaCRUD(self.db)
        self.categoria_crud = CategoriaCRUD(self.db)
        self.cliente_crud= ClienteCRUD(self.db)
        self.material_crud= MaterialBibliograficoCRUD(self.db)
        self.prestamo_crud= PrestamoCRUD(self.db)
        self.reserva_crud= ReservaCrud(self.db) 
        self.sancion_crud= SancionCRUD(self.db)
        self.usuario_actual: Optional[Usuario] = None
        self.sede_actual = None

    def crear_admin_si_no_existe(self):
        """
        Crea un usuario administrador por defecto si no existe.

        El administrador se crea con las siguientes credenciales:
            - nombre: "Administrador"
            - usuario: "admin"
            - email: "admin@system.com"
            - contraseña: "Admin1234!"
            - es_admin: True
        """
        from crud.Usuario_crud import UsuarioCRUD
        usuario_crud = UsuarioCRUD(self.db)
        if not usuario_crud.obtener_admin_por_defecto():
            admin = usuario_crud.crear_usuario(
                nombre="Administrador",
                nombre_usuario="admin",
                email="admin@system.com",
                contraseña="Admin1234!",
                es_admin=True
            )


    def __enter__(self):
        """
        Habilita el uso de `with SistemaGestion()` como context manager.

        Returns:
            SistemaGestion: Instancia actual del sistema.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Cierra la conexión de base de datos al salir del context manager.

        Args:
            exc_type (Type[BaseException]): Tipo de excepción (si ocurre).
            exc_val (BaseException): Instancia de la excepción (si ocurre).
            exc_tb (TracebackType): Traza de la excepción (si ocurre).
        """
        self.db.close()

    def mostrar_pantalla_login(self) -> bool:
        """
        Muestra la pantalla de inicio de sesión y gestiona el proceso de login.

        El usuario debe ingresar su nombre de usuario/email y contraseña.
        Se permite un máximo de 3 intentos.

        Returns:
            bool: 
                - True si el inicio de sesión fue exitoso.
                - False si se canceló la operación o se excedieron los intentos.
        """
        menu = (
            "\n" + "=" * 50 + "\n"
            "        SISTEMA BIBLIOTECARIO\n"
            + "=" * 50 + "\n"
            "INICIAR SESIÓN\n"
            + "=" * 50
        )
        messagebox.showinfo("Login", menu)

        intentos = 0
        max_intentos = 3

        while intentos < max_intentos:
            try:
                messagebox.showinfo("Intento", f"Intento {intentos + 1} de {max_intentos}")
                nombre_usuario = simpledialog.askstring("Login", "Nombre de usuario o email:")
                
                if nombre_usuario is None:  
                    messagebox.showinfo("Info", "Operación cancelada por el usuario")
                    return False
                nombre_usuario = nombre_usuario.strip()

                if not nombre_usuario:
                    messagebox.showerror("Error", "El nombre de usuario es obligatorio")
                    intentos += 1
                    continue

                contrasena = simpledialog.askstring("Login", "Contraseña:", show="*")

                if contrasena is None:  
                    messagebox.showinfo("Info", "Operación cancelada por el usuario")
                    return False
                
                if not contrasena:
                    messagebox.showerror("Error", "La contraseña es obligatoria")
                    intentos += 1
                    continue

                usuario = self.usuario_crud.autenticar_usuario(nombre_usuario, contrasena)

                if usuario:
                    self.usuario_actual = usuario
                    mensaje = f"¡Bienvenido, {usuario.nombre}!"
                    if usuario.es_admin:
                        mensaje += "\nTienes privilegios de administrador"
                    messagebox.showinfo("Éxito", mensaje)
                    return True
                else:
                    messagebox.showerror("Error", "Credenciales incorrectas o usuario inactivo")
                    intentos += 1

            except KeyboardInterrupt:
                messagebox.showerror("INFO", "Operacion cancelada por el usuario")
                return False
            except Exception as e:
                messagebox.showerror("Error", f"Error durante el login: {e}")
                intentos += 1

        messagebox.showerror("Error", f"Máximo de intentos ({max_intentos}) excedido. Acceso denegado.")
        return False

    def mostrar_menu_principal_autenticado(self) -> None:
        """
        Muestra el menú principal para un usuario autenticado.

        El menú permite acceder a diferentes secciones del sistema según el rol del usuario:
            1. Gestión de Usuarios (solo administradores).
            2. Gestión de Sedes.
            3. Gestión de Bibliotecas.
            4. Ver perfil del usuario.
            5. Elegir sede y acceder a su menú.
            0. Cerrar sesión.

        Returns:
            None
        """
        while True:
            menu_texto = (
                "\n" + "=" * 50 + "\n"
                "    SISTEMA BIBLIOTECARIO\n"
                + "=" * 50 + "\n"
                f"Usuario: {self.usuario_actual.nombre}\n"
                f"Email: {self.usuario_actual.email}\n"
            )
            if self.usuario_actual.es_admin:
                menu_texto += "Administrador\n"
            menu_texto += (
                "=" * 50 + "\n"
                "1. Gestión de Usuarios\n"
                "2. Gestión de Sedes\n"
                "3. Gestión de Bibliotecas\n"
                "4. Mi perfil\n"
                "5. Elegir sede\n"
                "0. Cerrar sesión\n"
                + "=" * 50
            )

            messagebox.showinfo("Menú Principal", menu_texto)
            opcion = simpledialog.askinteger("Menú Principal", "Ingrese el número de la opción:")
            if opcion is None or opcion == 0:
                messagebox.showinfo("Salir", "Sesión cerrada")
                break

            match opcion:
                case 1:
                    self.mostrar_menu_usuarios()
                case 2:
                    self.mostrar_menu_sede()
                case 3:
                    self.mostrar_menu_biblioteca()
                case 4:
                    messagebox.showinfo("Perfil", f"Mostrando perfil de {self.usuario_actual.nombre}")
                    self.mostrar_menu_perfil()
                case 5:
                    self.elegir_sede()
                    if self.sede_actual:
                        self.menu_sede()
                case _:
                    messagebox.showerror("Error", "Opción no válida")


    def mostrar_menu_usuarios(self) -> None:
        """
        Muestra el menú de gestión de usuarios.

        Permite realizar operaciones CRUD sobre usuarios:
            1. Crear Usuario.
            2. Listar Usuarios.
            3. Buscar Usuario por Email.
            4. Buscar Usuario por Nombre de Usuario.
            5. Actualizar Usuario.
            6. Eliminar Usuario.
            7. Crear Usuario Administrador.
            0. Volver al menú principal.

        Returns:
            None
        """
        while True:
            menu_texto = (
                "\n" + "-" * 30 + "\n"
                "   GESTION DE USUARIOS\n"
                + "-" * 30 + "\n"
                "1. Crear Usuario\n"
                "2. Listar Usuarios\n"
                "3. Buscar Usuario por Email\n"
                "4. Buscar Usuario por Nombre de Usuario\n"
                "5. Actualizar Usuario\n"
                "6. Eliminar Usuario\n"
                "7. Crear Usuario Administrador\n"
                "0. Volver al menú principal"
            )

            messagebox.showinfo("Menú Usuarios", menu_texto)

            opcion = simpledialog.askstring("Menú Usuarios", "Ingrese el número de la opción:")
            if opcion is None or opcion == "0":
                messagebox.showinfo("Salir", "Volviendo al menú principal")
                break

            match opcion.strip():
                case "1":
                    self.crear_usuario()
                case "2":
                    self.listar_usuarios()
                case "3":
                    self.buscar_usuario_por_email()
                case "4":
                    self.buscar_usuario_por_nombre_usuario()
                case "5":
                    self.actualizar_usuario()
                case "6":
                    self.eliminar_usuario()
                case "7":
                    self.crear_usuario_admin()
                case _:
                    messagebox.showerror("Error", "Opción no válida. Intente nuevamente.")

    def crear_usuario(self) -> None:
        """
        Crea un nuevo usuario en el sistema.

        Solicita al administrador la información necesaria mediante
        cuadros de diálogo y guarda el usuario en la base de datos.

        Returns:
            None
        """
        try:
            messagebox.showinfo("Crear Usuario", "--- CREAR USUARIO ---")

            nombre = simpledialog.askstring("Crear Usuario", "Nombre completo:")
            if nombre is None: return  

            nombre_usuario = simpledialog.askstring("Crear Usuario", "Nombre de usuario:")
            if nombre_usuario is None: return

            email = simpledialog.askstring("Crear Usuario", "Email:")
            if email is None: return

            contrasena = simpledialog.askstring("Crear Usuario", "Contraseña:", show="*")
            if contrasena is None: return

            telefono = simpledialog.askstring("Crear Usuario", "Teléfono (opcional):") or None
            es_admin_resp = simpledialog.askstring("Crear Usuario", "¿Es administrador? (s/n):")
            
            if es_admin_resp is None: return
            es_admin = es_admin_resp.strip().lower() == "s"

            usuario = self.usuario_crud.crear_usuario(
                nombre=nombre,
                nombre_usuario=nombre_usuario,
                email=email,
                contrasena=contrasena,
                telefono=telefono,
                es_admin=es_admin,
            )

            messagebox.showinfo("Éxito", f"Usuario creado exitosamente:\n{usuario}")

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def listar_usuarios(self) -> None:
        """
        Lista todos los usuarios registrados en el sistema.

        Muestra nombre, usuario, email, estado (activo/inactivo)
        y si es administrador.

        Returns:
            None
        """
        try:
            usuarios = self.usuario_crud.obtener_usuarios()
            if not usuarios:
                messagebox.showinfo("Usuarios", "No hay usuarios registrados.")
                return

            mensaje = f"--- USUARIOS ({len(usuarios)}) ---\n"
            for i, usuario in enumerate(usuarios, 1):
                admin_text = " (ADMIN)" if usuario.es_admin else ""
                activo_text = "Activo" if usuario.activo else "Inactivo"
                mensaje += (
                    f"{i}. {usuario.nombre} ({usuario.nombre_usuario}) - {usuario.email} - {activo_text}{admin_text}\n"
                )

            messagebox.showinfo("Usuarios", mensaje)

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def buscar_usuario_por_email(self) -> None:
        """
        Busca un usuario por su dirección de email.

        Solicita el email mediante un cuadro de diálogo y muestra
        la información si el usuario existe.

        Returns:
            None
        """
        try:
            email = simpledialog.askstring("Buscar Usuario", "Ingrese el email a buscar:")
            if email is None:  # Usuario canceló
                return
            email = email.strip()

            usuario = self.usuario_crud.obtener_usuario_por_email(email)

            if usuario:
                admin_text = " (ADMIN)" if usuario.es_admin else ""
                activo_text = "Activo" if usuario.activo else "Inactivo"
                mensaje = (
                    "EXITO: Usuario encontrado:\n"
                    f"Nombre: {usuario.nombre}\n"
                    f"Nombre de usuario: {usuario.nombre_usuario}\n"
                    f"Email: {usuario.email}\n"
                    f"Telefono: {usuario.telefono or 'No especificado'}\n"
                    f"Estado: {activo_text}{admin_text}"
                )
                messagebox.showinfo("Usuario encontrado", mensaje)
            else:
                messagebox.showerror("Error", "Usuario no encontrado.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def buscar_usuario_por_nombre_usuario(self) -> None:
        """
        Busca un usuario por su nombre de usuario.

        Solicita el nombre de usuario mediante un cuadro de diálogo
        y muestra la información si el usuario existe.

        Returns:
            None
        """
        try:
            nombre_usuario = simpledialog.askstring(
                "Buscar Usuario", "Ingrese el nombre de usuario a buscar:"
            )
            if nombre_usuario is None: 
                return
            nombre_usuario = nombre_usuario.strip()

            usuario = self.usuario_crud.obtener_usuario_por_nombre_usuario(nombre_usuario)

            if usuario:
                admin_text = " (ADMIN)" if usuario.es_admin else ""
                activo_text = "Activo" if usuario.activo else "Inactivo"
                mensaje = (
                    "EXITO: Usuario encontrado:\n"
                    f"Nombre: {usuario.nombre}\n"
                    f"Nombre de usuario: {usuario.nombre_usuario}\n"
                    f"Email: {usuario.email}\n"
                    f"Telefono: {usuario.telefono or 'No especificado'}\n"
                    f"Estado: {activo_text}{admin_text}"
                )
                messagebox.showinfo("Usuario encontrado", mensaje)
            else:
                messagebox.showerror("Error", "Usuario no encontrado.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def actualizar_usuario(self) -> None:
        """
        Actualiza la información de un usuario existente.

        Solicita el email del usuario y permite modificar los campos
        nombre, usuario, email y teléfono.

        Returns:
            None
        """
        try:
            email = simpledialog.askstring("Actualizar Usuario", "Ingrese el email del usuario a actualizar:")
            if email is None:  # Cancelado
                return
            email = email.strip()

            usuario = self.usuario_crud.obtener_usuario_por_email(email)

            if not usuario:
                messagebox.showerror("Error", "Usuario no encontrado.")
                return

            messagebox.showinfo("Actualizar Usuario", f"Actualizando usuario: {usuario.nombre}\n\nDeje en blanco para mantener el valor actual.")

            nuevo_nombre = simpledialog.askstring("Actualizar Usuario", f"Nombre actual ({usuario.nombre}):") or ""
            nuevo_nombre_usuario = simpledialog.askstring("Actualizar Usuario", f"Nombre de usuario actual ({usuario.nombre_usuario}):") or ""
            nuevo_email = simpledialog.askstring("Actualizar Usuario", f"Email actual ({usuario.email}):") or ""
            nuevo_telefono = simpledialog.askstring("Actualizar Usuario", f"Teléfono actual ({usuario.telefono or 'No especificado'}):") or ""

            cambios = {}
            if nuevo_nombre.strip():
                cambios["nombre"] = nuevo_nombre.strip()
            if nuevo_nombre_usuario.strip():
                cambios["nombre_usuario"] = nuevo_nombre_usuario.strip()
            if nuevo_email.strip():
                cambios["email"] = nuevo_email.strip()
            if nuevo_telefono.strip():
                cambios["telefono"] = nuevo_telefono.strip()

            if cambios:
                usuario_actualizado = self.usuario_crud.actualizar_usuario(usuario.id, **cambios)
                messagebox.showinfo("Éxito", f"Usuario actualizado:\n{usuario_actualizado}")
            else:
                messagebox.showinfo("Sin cambios", "No se realizaron modificaciones.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

    def eliminar_usuario(self) -> None:
        """
        Elimina un usuario del sistema.

        Solicita el email del usuario y pide confirmación antes de eliminarlo.

        Returns:
            None
        """
        try:
            email = simpledialog.askstring("Eliminar Usuario", "Ingrese el email del usuario a eliminar:")
            if email is None:  
                return
            email = email.strip()

            usuario = self.usuario_crud.obtener_usuario_por_email(email)

            if not usuario:
                messagebox.showerror("Error", "Usuario no encontrado.")
                return

            # askyesno propio de tkinder, muestra una ventana con botones de si y no, retorna un booleano
            confirmacion = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar a {usuario.nombre}?"
            )

            if confirmacion:
                if self.usuario_crud.eliminar_usuario(usuario.id):
                    messagebox.showinfo("Éxito", "Usuario eliminado exitosamente.")
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el usuario.")
            else:
                messagebox.showinfo("Cancelado", "Operación cancelada.")

        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

    def crear_usuario_admin(self) -> None:
        """
        Crea un usuario administrador por defecto.

        Si ya existe un administrador predeterminado, muestra un mensaje.
        En caso contrario, genera un usuario admin con contraseña temporal.

        Returns:
            None
        """
        try:
            admin = self.usuario_crud.obtener_admin_por_defecto()
            if admin:
                messagebox.showinfo("Información", "Ya existe un usuario administrador por defecto.")
                return

            contrasena_admin = PasswordManager.generate_secure_password(12)
            admin = self.usuario_crud.crear_usuario(
                nombre="Administrador del Sistema",
                nombre_usuario="admin",
                email="admin@system.com",
                contrasena=contrasena_admin,
                es_admin=True,
            )

            messagebox.showinfo("Éxito", f"Usuario administrador creado:\n{admin}")
            messagebox.showinfo(
                "Contraseña temporal", 
                f"Contraseña temporal: {contrasena_admin}\n\n"
                "IMPORTANTE: Cambie esta contraseña en su primer inicio de sesión."
            )

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")


    def mostrar_menu_sede(self):
        """
        Muestra el menú de gestión de sedes.

        Permite realizar operaciones CRUD sobre sedes:
            1. Crear Sede.
            2. Listar Sedes.
            3. Buscar Sede por nombre.
            4. Eliminar Sede.
            5. Actualizar Sede.
            0. Volver al menú principal.

        Returns:
            None
        """
        while True:
            menu_texto = (
                "\n" + "-" * 30 + "\n"
                "   GESTION DE SEDES\n"
                + "-" * 30 + "\n"
                "1. Crear Sede\n"
                "2. Listar Sedes\n"
                "3. Buscar Sede por nombre\n"
                "4. Eliminar Sede\n"
                "5. Actulizar sede\n"
                "0. Volver al menú principal"
            )

            messagebox.showinfo("Menú Sedes", menu_texto)

            opcion = simpledialog.askstring("Menú Sedes", "Ingrese el número de la opción:")
            if opcion is None or opcion == "0":
                messagebox.showinfo("Salir", "Volviendo al menú principal")
                break

            match opcion.strip():
                case "1":
                    self.crear_sede()
                case "2":
                    self.listar_sedes()
                case "3":
                    self.buscar_sede_por_nombre()
                case "4":
                    self.eliminar_sede()
                case "5":
                    self.actualizar_sede()
                case _:
                    messagebox.showerror("Error", "Opción no válida. Intente nuevamente.")

    def crear_sede(self) -> None:
        """
        Crea una nueva sede en el sistema.

        Solicita al usuario el nombre y la dirección de la sede.
        Verifica que no exista una sede con el mismo nombre antes
        de guardarla en la base de datos.

        Returns:
            None
        """
        try:
            messagebox.showinfo("Crear Sede", "--- CREAR SEDE ---")

            nombre = simpledialog.askstring("Crear Sede", "Nombre de la sede:")
            if nombre is None: return
            nombre = nombre.strip()

            existente = self.sede_crud.obtener_sede_por_nombre(nombre)
            if existente:
                messagebox.showerror("Error", f"Ya existe una sede con el nombre '{nombre}'.")
                return

            direccion = simpledialog.askstring("Crear Sede", "Direccion de la sede:")
            if direccion is None: return
            direccion = direccion.strip()
            
            sede = self.sede_crud.crear_sede(
                nombre=nombre.strip().lower(),
                direccion=direccion,
                id_usuario_crea=self.usuario_actual.id_usuario if self.usuario_actual else None
            )
            
            messagebox.showinfo("Éxito", f"Sede creada exitosamente:\n" 
                                         f"Sede: {sede.nombre}\n"
                                         f"ID: {sede.id_sede}"
                                         )

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")
            
    def listar_sedes(self) -> None:
        """
        Lista todas las sedes registradas en el sistema.

        Muestra el identificador, nombre y dirección de cada sede.

        Returns:
            None
        """
        try:
            sedes = self.sede_crud.obtener_sedes()
            if not sedes:
                messagebox.showinfo("Sedes", "No hay sedes registrados.")
                return

            mensaje = f"--- SEDES REGISTRADAS ({len(sedes)}) ---\n\n"
            for i, sede in enumerate(sedes, 1):
                mensaje += (
                    f"{i}. ID Sede: {sede.id_sede}\n"
                    f"     Nombre: {sede.nombre}\n"
                    f"     Dirección: {sede.direccion}\n"
                )

            messagebox.showinfo("Sedes", mensaje)

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def buscar_sede_por_nombre(self) -> None:
        """
        Busca una sede por su nombre.

        Solicita el nombre de la sede y muestra su información
        si existe en la base de datos.

        Returns:
            None
        """
        try:
            nombre = simpledialog.askstring("Buscar Sede", "Ingrese el nombre a buscar:")
            if nombre is None:
                return
            nombre = nombre.strip().lower()

            sede = self.sede_crud.obtener_sede_por_nombre(nombre)

            if sede:
                mensaje = (
                    "EXITO: Sede encontrada:\n\n"
                    f"Id: {sede.id_sede}\n"
                    f"Nombre: {sede.nombre}\n"
                    f"Dirección: {sede.direccion}\n"
                )
                messagebox.showinfo("Sede encontrada", mensaje)
            else:
                messagebox.showerror("Error", f"No existe una sede con el nombre '{nombre}'.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def actualizar_sede(self) -> None:
        """
        Actualiza la información de una sede existente.

        Permite modificar el nombre y la dirección de la sede.
        Si se dejan campos en blanco, se conservan los valores actuales.

        Returns:
            None
        """
        try:
            sede = self.seleccionar_sede()
            if not sede:
                return

            messagebox.showinfo("Actualizar Sede", f"Actualizando sede: {sede.nombre}\n\nDeje en blanco para mantener el valor actual.")

            nuevo_nombre = simpledialog.askstring("Actualizar Sede", f"Nombre actual ({sede.nombre}):") or ""
            nueva_direccion = simpledialog.askstring("Actualizar Sede", f"Direccion actual ({sede.direccion}):") or ""
            
            cambios = {}
            if nuevo_nombre.strip().lower():
                cambios["nombre"] = nuevo_nombre.strip().lower()
            if nueva_direccion.strip():
                cambios["direccion"] = nueva_direccion.strip()

            if cambios:
                sede_actualizada = self.sede_crud.actualizar_sede(sede.id_sede, **cambios)
                mensaje = (
                    "Sede actualizada con éxito:\n\n"
                    f"ID: {sede_actualizada.id_sede}\n"
                    f"Nombre: {sede_actualizada.nombre}\n"
                    f"Dirección: {sede_actualizada.direccion}"
                )
                messagebox.showinfo("Éxito", mensaje)
            else:
                messagebox.showinfo("Sin cambios", "No se realizaron modificaciones.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

    def eliminar_sede(self) -> None:
        """
        Elimina una sede del sistema.

        Solicita confirmación antes de proceder. 
        Si la sede está relacionada con otros registros,
        puede lanzar un error por restricciones de integridad.

        Returns:
            None
        """
        try:
            sede = self.seleccionar_sede()
            if not sede:
                return
            
            confirmacion = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar a {sede.nombre} (Id: {sede.id_sede})?\n\n"
                "Esta acción no se puede deshacer."
            )

            if confirmacion:
                try:
                    if self.sede_crud.eliminar_sede(sede.id_sede):
                        messagebox.showinfo("Éxito", "Sede eliminada exitosamente.")
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar la sede.")
                except Exception as e:
                    # Posible error por restricciones de integridad
                    messagebox.showerror("Error", f"No se pudo eliminar la sede.\nDetalle: {e}")
            else:
                messagebox.showinfo("Cancelado", "Operación cancelada.")

        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")
    
#-------------------------------------------------------
# MENU BIBLIOTECA
#-------------------------------------------------------
    """
        Muestra el menú de gestión de bibliotecas.

        Permite realizar operaciones CRUD sobre biblioteca:
            1. Crear biblioteca.
            2. Listar bibliotecas.
            3. Buscar biblioteca por id.
            4. buscar biblioteca por nombre
            5. actualizar biblioteca
            6. Eliminar biblioteca
            0. Volver al menú principal.

        Returns:
            None
    """
    def mostrar_menu_biblioteca(self) -> None:
        while True:
            menu_texto = (
                "\n" + "-" * 30 + "\n"
                "   GESTION DE BIBLIOTECAS\n"
                + "-" * 30 + "\n"
                "1. Crear Biblioteca\n"
                "2. Listar Bibliotecas\n"
                "3. Buscar biblioteca por ID\n"
                "4. Buscar biblioteca por nombre\n"
                "5. Actualizar biblioteca\n"
                "6. Eliminar biblioteca\n"
                "0. Volver al menú principal"
            )

            messagebox.showinfo("Menú biblioteca", menu_texto)

            opcion = simpledialog.askstring("Menú Bibliotecas", "Ingrese el número de la opción:")
            if opcion is None or opcion == "0":
                messagebox.showinfo("Salir", "Volviendo al menú principal")
                break

            match opcion.strip():
                case "1":
                    self.crear_biblioteca()
                case "2":
                    self.obtener_bibliotecas()
                case "3":
                    self.obtener_biblioteca()
                case "4":
                    self.obtener_biblioteca_por_nombre()
                case "5":
                    self.actualizar_biblioteca()
                case "6":
                    self.eliminar_biblioteca()
                case _:
                    messagebox.showerror("Error", "Opción no válida. Intente nuevamente.")

    def crear_biblioteca(self) -> None:
        """
        Crea una nueva biblioteca en el sistema.

        Solicita al usuario el nombre de la biblioteca.
        Verifica que no exista una biblioteca con el mismo nombre antes
        de guardarla en la base de datos.

        Returns:
            None"""
        try:
            messagebox.showinfo("Crear Biblioteca", "--- CREAR BIBLIOTECA ---")

            sedes = self.sede_crud.obtener_sedes()
            if not sedes:
                messagebox.showerror("Error", "No hay sedes registradas. Crea una sede primero.")
                return

            nombres_sedes = [sede.nombre for sede in sedes]
            nombre_sede = simpledialog.askstring("Seleccionar Sede", f"Sedes disponibles:\n{', '.join(nombres_sedes)}\n\nEscriba el nombre de la sede:")

            if not nombre_sede:
                return

            sede = self.sede_crud.obtener_sede_por_nombre(nombre_sede)
            if not sede:
                messagebox.showerror("Error", f"No se encontró una sede llamada '{nombre_sede}'")
                return

            nombre = simpledialog.askstring("Crear Biblioteca", "Nombre de la Biblioteca:")
            if nombre is None: return  
            nombre = nombre.strip().lower()

            biblioteca = self.biblioteca_crud.crear_biblioteca(
                nombre=nombre,
                id_sede= sede.id_sede,
                id_usuario_crea=self.usuario_actual.id_usuario if self.usuario_actual else None
            )

            messagebox.showinfo("Éxito", f"Biblioteca creada:\n"
                                         f"Biblioteca: {biblioteca.nombre}\n"
                                         f"ID: {biblioteca.id_biblioteca}")

            self.biblioteca_actual = biblioteca

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")
            
    def obtener_bibliotecas(self) -> None:

        """Lista todas las bibliotecas del sistema.
        Muestra en pantalla todas las bibliotecas creadas
        Returns None"""

        try:
            bibliotecas = self.biblioteca_crud.obtener_bibliotecas()
            if not bibliotecas:
                messagebox.showinfo("Bibliotecas", "No hay bibliotecas registrados.")
                return

            mensaje = f"--- BIBLIOTECAS  ({len(bibliotecas)}) ---\n\n"
            for i, biblioteca in enumerate(bibliotecas, 1):
                mensaje += (
                    f"{i}. {biblioteca.nombre}\n"
                    f"   Nombre: {biblioteca.nombre}\n"
                    f"   Sede: {biblioteca.id_sede}\n\n"
                )

            messagebox.showinfo("Bibliotecas", mensaje)

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def obtener_biblioteca(self) -> None:

        """ Busca una biblioteca por ID.
        Se le pide al usuario ingresar el ID de la biblioteca para buscarla

        returns None"""
        try:
            biblioteca = self.seleccionar_biblioteca()
            if not biblioteca:
                messagebox.showerror("Error", "No se seleccionó ninguna biblioteca o no hay bibliotecas registradas.")
                return
            sede = cast(Sede, biblioteca.sede)
            mensaje = (
                    "EXITO: Biblioteca encontrada:\n"
                    f"ID: {biblioteca.id_biblioteca}\n"
                    f"Nombre: {biblioteca.nombre}\n"
                    f"Sede: {sede.nombre}"
                    
            )
            messagebox.showinfo("Biblioteca encontrada", mensaje)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def obtener_biblioteca_por_nombre(self) -> None:

        """Busca una biblioteca por el nombre.
        Se le pide al usuario ingresar el nombre de la biblioteca para buscarla
        Returns None"""
        try:
            nombre = simpledialog.askstring("Buscar biblioteca", "Ingrese el nombre a buscar:")
            if nombre is None: return
            nombre = nombre.strip()

            biblioteca = self.biblioteca_crud.obtener_biblioteca_por_nombre(nombre)

            if biblioteca:
                mensaje = (
                    "EXITO: Biblioteca encontrada:\n"
                    f"ID: {biblioteca.id_biblioteca}\n"
                    f"Nombre: {biblioteca.nombre}\n"
                    f"Sede: {biblioteca.id_sede}"
                )
                messagebox.showinfo("Biblioteca encontrada", mensaje)
            else:
                messagebox.showerror("Error", "Biblioteca no encontrada.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def actualizar_biblioteca(self) -> None:

        """Actualiza una biblioteca.
        Se le pide al usuario ingresar el nombre actual de la biblioteca para buscarla, si esta se encuentra se le pide
        un nuevo nombre para esta biblioteca
        
        Returns None"""
        try:
            nombre = simpledialog.askstring("Actualizar Biblioteca", "Ingrese el nombre de la biblioteca a actualizar:")
            if nombre is None: return
            nombre = nombre.strip()

            biblioteca = self.biblioteca_crud.obtener_biblioteca_por_nombre(nombre)

            if not biblioteca:
                messagebox.showerror("Error", f"No existe una biblioteca con el nombre '{nombre}'.")
                return

            messagebox.showinfo("Actualizar Biblioteca", f"Actualizando Biblioteca: {biblioteca.nombre}\n\nDeje en blanco para mantener el valor actual.")
            
            nuevo_nombre = simpledialog.askstring("Actualizar Biblioteca", f"Nombre actual ({biblioteca.nombre}):") or ""
            cambios = {}
            if nuevo_nombre.strip():
                cambios["nombre"] = nuevo_nombre.strip()

            if cambios:
                biblioteca_actualizada = self.biblioteca_crud.actualizar_biblioteca(biblioteca.id_biblioteca, **cambios)
                mensaje = ("Biblioteca actualizada:\n\n"
                    f"ID: {biblioteca_actualizada.id_biblioteca}\n"
                    f"Nombre: {biblioteca_actualizada.nombre}\n"
                    f"Sede: {biblioteca_actualizada.id_sede}"
                )
                messagebox.showinfo("Biblioteca actualizada", mensaje)
            else:
                messagebox.showinfo("Sin cambios", "No se realizaron modificaciones.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

    def eliminar_biblioteca(self) -> None:

        """Elimina una biblioteca.
        Se le pide al usuario ingresar ek nombre de la biblioteca para buscarla, si esta se encuentra el usuario debe decidir
        si eliminarla o no, si elije si, se elimina del sistema.
        
        Returns None"""
        try:
            nombre = simpledialog.askstring("Eliminar Biblioteca", "Ingrese el nombre de la biblioteca a eliminar:")
            if nombre is None:  
                return
            nombre = nombre.strip()

            biblioteca = self.biblioteca_crud.obtener_biblioteca_por_nombre(nombre)

            if not biblioteca:
                messagebox.showerror("Error", "Biblioteca no encontrada.")
                return

            confirmacion = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar a la biblioteca {biblioteca.id_biblioteca}: {biblioteca.nombre}?"
            )

            if confirmacion:
                if self.biblioteca_crud.eliminar_biblioteca(biblioteca):
                    messagebox.showinfo("Éxito", f"Biblioteca '{biblioteca.nombre}' eliminada exitosamente.")
                else:
                    messagebox.showerror("Error", "No se pudo eliminar la biblioteca.")
            else:
                messagebox.showinfo("Cancelado", "Operación cancelada.")

        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

#-------------------------------------------------------
# MENU PERFIL
#-------------------------------------------------------
    """
        Muestra el menú de gestión de perfil.

            1. Ver infromacion personal.
            2. Actualizar informacion.
            3. cambiar la contraseña."""
    
    def mostrar_menu_perfil(self) -> None:
        """Mostrar menú de perfil del usuario"""
        while True:
            menu_texto = (
                "\n" + "-" * 30 + "\n"
                "        MI PERFIL\n"
                + "-" * 30 + "\n"
                "1. Ver Información Personal\n"
                "2. Actualizar Información\n"
                "3. Cambiar Contraseña\n"
                "0. Volver al menú principal\n"
            )

            messagebox.showinfo("Menú Perfil", menu_texto)
            opcion = simpledialog.askstring("Menú Perfil", "Seleccione una opción:")

            if opcion is None:
                messagebox.showinfo("Salir", "Regresando al menú principal")
                break

            match opcion.strip():
                case "1":
                    self.ver_informacion_personal()
                case "2":
                    self.actualizar_informacion_personal()
                case "3":
                    self.cambiar_contrasena()
                case "0":
                    messagebox.showinfo("Salir", "Vuelves al menú principal")
                    break
                case _:
                    messagebox.showerror("Error", "Opción inválida. Intente nuevamente.")

    def ver_informacion_personal(self) -> None:
        """Ver información personal del usuario"""
        try:
            info = (
                "--- INFORMACIÓN PERSONAL ---\n"
                f"Nombre: {self.usuario_actual.nombre}\n"
                f"Nombre de usuario: {self.usuario_actual.nombre_usuario}\n"
                f"Email: {self.usuario_actual.email}\n"
                f"Teléfono: {self.usuario_actual.telefono or 'No especificado'}\n"
                f"Estado: {'Activo' if self.usuario_actual.activo else 'Inactivo'}\n"
                f"Rol: {'Administrador' if self.usuario_actual.es_admin else 'Usuario'}\n"
                f"Fecha de creación: {self.usuario_actual.fecha_creacion}\n"
            )

            messagebox.showinfo("Mi Perfil", info)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al mostrar la información personal:\n{e}")

    def actualizar_informacion_personal(self) -> None:
        """Actualizar información personal del usuario"""
        try:
            messagebox.showinfo(
                "Actualizar Información Personal",
                "Deja en blanco para mantener el valor actual."
            )

            nuevo_nombre = simpledialog.askstring(
                "Actualizar", f"Nombre actual ({self.usuario_actual.nombre}):"
            )
            nuevo_nombre_usuario = simpledialog.askstring(
                "Actualizar", f"Nombre de usuario actual ({self.usuario_actual.nombre_usuario}):"
            )
            nuevo_email = simpledialog.askstring(
                "Actualizar", f"Email actual ({self.usuario_actual.email}):"
            )
            nuevo_telefono = simpledialog.askstring(
                "Actualizar", f"Teléfono actual ({self.usuario_actual.telefono or 'No especificado'}):"
            )

            cambios = {}
            if nuevo_nombre:
                cambios["nombre"] = nuevo_nombre.strip()
            if nuevo_nombre_usuario:
                cambios["nombre_usuario"] = nuevo_nombre_usuario.strip()
            if nuevo_email:
                cambios["email"] = nuevo_email.strip()
            if nuevo_telefono:
                cambios["telefono"] = nuevo_telefono.strip()

            if cambios:
                usuario_actualizado = self.usuario_crud.actualizar_usuario(
                    self.usuario_actual.id, **cambios
                )
                if usuario_actualizado:
                    self.usuario_actual = usuario_actualizado
                    messagebox.showinfo("Éxito", "Información actualizada exitosamente.")
                else:
                    messagebox.showerror("Error", "No se pudo actualizar la información.")
            else:
                messagebox.showinfo("Sin cambios", "No se realizaron cambios.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error de validación: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def cambiar_contrasena(self) -> None:
        """Cambiar contraseña del usuario"""
        try:
            messagebox.showinfo("Cambiar Contraseña", "Ingrese la información solicitada")

            contrasena_actual = simpledialog.askstring(
                "Contraseña Actual", "Ingrese su contraseña actual:", show="*"
            )
            if not contrasena_actual:
                messagebox.showerror("Error", "La contraseña actual es obligatoria.")
                return

            nueva_contrasena = simpledialog.askstring(
                "Nueva Contraseña", "Ingrese la nueva contraseña:", show="*"
            )
            if not nueva_contrasena:
                messagebox.showerror("Error", "La nueva contraseña es obligatoria.")
                return

            confirmar_contrasena = simpledialog.askstring(
                "Confirmar Contraseña", "Confirme la nueva contraseña:", show="*"
            )
            if nueva_contrasena != confirmar_contrasena:
                messagebox.showerror("Error", "Las contraseñas no coinciden.")
                return

            if self.usuario_crud.cambiar_contraseña(
                self.usuario_actual.id, contrasena_actual, nueva_contrasena
            ):
                messagebox.showinfo("Éxito", "Contraseña cambiada exitosamente.")
            else:
                messagebox.showerror("Error", "Error al cambiar la contraseña.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error de validación: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

#-------------------------------------------------------
# MENU ELEGIR SEDE
#-------------------------------------------------------
    """ Eleccion de sede"""
    def elegir_sede(self):
        sedes_db = self.sede_crud.obtener_sedes()
        if not sedes_db:
            messagebox.showinfo("Info", "No hay sedes registradas")
            return

        opciones = "\n--- SEDES DISPONIBLES ---\n"
        for i, sede in enumerate(sedes_db, start=1):
            opciones += f"{i}. {sede.nombre} ({sede.direccion})\n"

        opcion = simpledialog.askinteger("Elegir sede", opciones)
        if opcion is None:
            return

        if 1 <= opcion <= len(sedes_db):
            sede_elegida = sedes_db[opcion - 1]
            
            if not sede_elegida.id_sede:
                messagebox.showerror(
                    "Error",
                    f"La sede '{sede_elegida.nombre}' no tiene un ID válido para asociar biblioteca"
                )
                return

            self.sede_actual = sede_elegida 

            biblioteca = self.biblioteca_crud.obtener_biblioteca_por_sede(sede_elegida.id_sede)

            if biblioteca:
                self.biblioteca_actual = biblioteca
                messagebox.showinfo(
                    "Sede seleccionada",
                    f"Sede activa: {sede_elegida.nombre}\nBiblioteca: {biblioteca.nombre}"
                )
            else:
                self.biblioteca_actual = None
                messagebox.showwarning(
                    "Advertencia",
                    f"La sede '{sede_elegida.nombre}' no tiene biblioteca asociada."
                )
        else:
            messagebox.showerror("Error", "Opción inválida")

    """
        Muestra el menú de sedes.
            1. Gestion de clientes.
            2. Gestion de categorias.
            3. Gestión de Material bibliográfico.
            4. Gestion de reservas.
            5. gestion de prestamos.
            6. gestion de sanciones"""
    def menu_sede(self):
        opcion = -1
        while opcion != 0:
            titulo = f"--- Menú Biblioteca {self.biblioteca_actual.nombre if self.biblioteca_actual else 'Ninguna'} / Sede {self.sede_actual.nombre} ---\n"

            menu = (
                titulo +
                "1. Gestión de Clientes\n"
                "2. Gestión de Categorías\n"
                "3. Gestión de Material bibliográfico\n"
                "4. Gestión de Reservas\n"
                "5. Gestión de Préstamos\n"
                "6. Gestión de Sanciones\n"
                "0. Volver a elección de Sede\n"
            )
            resp = simpledialog.askinteger("Menú Principal", menu)
            if resp is None: 
                break
        
            opcion= int(resp)
            match opcion:
                case 0: 
                    break
                case 1: 
                    self.mostrar_menu_cliente()
                case 2:
                    self.mostrar_menu_categoria()
                case 3: 
                    self.mostrar_menu_material()
                case 4: 
                    self.mostrar_menu_reserva()
                case 5: 
                    self.mostrar_menu_prestamo()
                case 6: 
                    self.mostrar_menu_sanciones()
                case _: 
                    messagebox.showerror("Error", "Opción no válida")


#-------------------------------------------------------
# SELECCIONAR
#-------------------------------------------------------
    """Permite al usuario seleccionar un cliente de la biblioteca indicada.
        Retorna el objeto cliente o None si el usuario cancela o no hay clientes."""
    def seleccionar_cliente(self, id_biblioteca: UUID) -> Optional[Cliente]:
        clientes = self.cliente_crud.obtener_clientes(id_biblioteca)
        if not clientes:
            messagebox.showinfo("Info", "No hay clientes registrados en esta biblioteca")
            return None

        opciones = "\n--- CLIENTES DISPONIBLES ---\n"
        opciones += "\n--- Ingrese el cliente para realizar la operacion ---\n\n"
        for i, cliente in enumerate(clientes, start=1):
            opciones += f"{i}. {cliente.nombre} ({cliente.tipo_cliente})\n"

        opcion = simpledialog.askinteger("Seleccionar Cliente", opciones)
        if opcion is None or opcion < 1 or opcion > len(clientes):
            return None

        return clientes[opcion - 1] 
    
    def seleccionar_material(self, id_biblioteca: UUID) -> Optional[Material_Bibliografico]:
        """
        Permite al usuario seleccionar un material bibliográfico de la biblioteca indicada.
        Retorna el objeto Material_Bibliografico o None si el usuario cancela o no hay materiales.
        """

        materiales = self.material_crud.obtener_materiales(id_biblioteca)
        if not materiales:
            messagebox.showinfo("Info", "No hay materiales registrados en esta biblioteca")
            return None

        opciones = "\n--- MATERIALES DISPONIBLES ---\n"
        opciones += "\n--- Ingrese el material para realizar la operacion ---\n\n"
        for i, material in enumerate(materiales, start=1):
            opciones += f"{i}. {material.titulo} - {material.autor or 'Autor desconocido'} ({material.estado or 'Sin estado'})\n"

        opcion = simpledialog.askinteger("Seleccionar Material", opciones)
        if opcion is None or opcion < 1 or opcion > len(materiales):
            return None

        return materiales[opcion - 1]

    def seleccionar_categoria(self, id_biblioteca: UUID) -> Optional[Categoria]:
        """
        Permite al usuario seleccionar una categoría de la biblioteca indicada.
        Retorna el objeto Categoria o None si el usuario cancela o no hay categorías.
        """
        categorias = self.categoria_crud.obtener_categorias(id_biblioteca)
        if not categorias:
            messagebox.showinfo("Info", "No hay categorías registradas en esta biblioteca")
            return None

        opciones = "\n--- CATEGORÍAS DISPONIBLES ---\n"
        opciones += "\n--- Ingrese la categoría para realizar la operacion ---\n\n"
        for i, categoria in enumerate(categorias, start=1):
            opciones += f"{i}. {categoria.nombre} ({categoria.descripcion or 'Sin descripción'})\n"

        opcion = simpledialog.askinteger("Seleccionar Categoría", opciones)
        if opcion is None or opcion < 1 or opcion > len(categorias):
            return None

        return categorias[opcion - 1]
    
    """Permite al usuario seleccionar una reserva de la biblioteca indicada.
        Retorna el objeto reserva o None si el usuario cancela o no hay reservas."""
    def seleccionar_reserva(self, id_biblioteca: UUID) -> Optional[Reserva]:
        reservas = self.reserva_crud.obtener_reservas(id_biblioteca)

        if not reservas:
            messagebox.showinfo("Info", "No hay reservas registradas en esta biblioteca")
            return None

        opciones = "\n--- RESERVAS DISPONIBLES ---\n"
        for i, reserva in enumerate(reservas, start=1):
            cliente = cast(Cliente, reserva.cliente)
            material = cast(Material_Bibliografico, reserva.material)
            
            opciones += (f"{i}. Material: {material.titulo}\n"
                         f"     Cliente: {cliente.nombre}\n"
                         f"     Estado: {reserva.estado}\n")

        opcion = simpledialog.askinteger("Seleccionar Reserva", opciones)
        if opcion is None or opcion < 1 or opcion > len(reservas):
            return None

        return reservas[opcion - 1]

    """Permite al usuario seleccionar un prestamo de la biblioteca indicada.
        Retorna el objeto prestamo o None si el usuario cancela o no hay prestamos."""
    def seleccionar_prestamo(self, id_biblioteca: UUID) -> Optional[Prestamo]:
        prestamos = self.prestamo_crud.obtener_prestamos(id_biblioteca)

        if not prestamos:
            messagebox.showinfo("Info", "No hay préstamos registrados en esta biblioteca")
            return None

        opciones = "\n--- PRÉSTAMOS DISPONIBLES ---\n"
        for i, prestamo in enumerate(prestamos, start=1):
            cliente = cast(Cliente, prestamo.cliente)
            material = cast(Material_Bibliografico, prestamo.material)
            opciones += (
                f"{i}. Material: {material.titulo}\n"
                f"     Cliente: {cliente.nombre}\n"
                f"     Préstamo: {prestamo.fecha_prestamo}\n"
                f"     Entrega: {prestamo.fecha_entrega}\n"
            )


        opcion = simpledialog.askinteger("Seleccionar Préstamo", opciones)
        if opcion is None or opcion < 1 or opcion > len(prestamos):
            return None

        return prestamos[opcion - 1]

    def seleccionar_sancion(self, id_biblioteca: UUID) -> Optional[Sancion]:
        """
        Permite al usuario seleccionar una sanción de la biblioteca indicada.
        Retorna el objeto Sancion o None si el usuario cancela o no hay sanciones.
        """
        sanciones = self.sancion_crud.obtener_sanciones(id_biblioteca)
        if not sanciones:
            messagebox.showinfo("Info", "No hay sanciones registradas en esta biblioteca")
            return None

        opciones = "\n--- SANCIONES DISPONIBLES ---\n"
        opciones += "\n--- Ingrese la sanción para realizar la operacion ---\n\n"
        for i, sancion in enumerate(sanciones, start=1):
            cliente = cast(Cliente, sancion.cliente)
            opciones += (
                f"{i}. Cliente: {cliente.nombre}\n"
                f"     Motivo: {sancion.motivo}\n"
                f"     Estado: {'Activa'}\n\n"
            )

        opcion = simpledialog.askinteger("Seleccionar Sanción", opciones)
        if opcion is None or opcion < 1 or opcion > len(sanciones):
            return None

        return sanciones[opcion - 1]

    def seleccionar_sede(self) -> Optional[Sede]:
        """
        Permite al usuario seleccionar una sede de la base de datos.
        Retorna el objeto Sede o None si el usuario cancela o no hay sedes.
        """
        sedes = self.sede_crud.obtener_sedes()
        if not sedes:
            messagebox.showinfo("Info", "No hay sedes registradas en el sistema")
            return None

        opciones = "\n--- SEDES DISPONIBLES ---\n"
        opciones += "\n--- Ingrese la sede para realizar la operación ---\n\n"
        for i, sede in enumerate(sedes, start=1):
            opciones += f"{i}. {sede.nombre} ({sede.direccion or 'Sin dirección'})\n"

        opcion = simpledialog.askinteger("Seleccionar Sede", opciones)
        if opcion is None or opcion < 1 or opcion > len(sedes):
            return None

        return sedes[opcion - 1]

    """Permite al usuario seleccionar una biblioteca de la lista indicada.
        Retorna el objeto biblioteca o None si el usuario cancela o no hay biblioteca."""
    def seleccionar_biblioteca(self) -> Optional[Biblioteca]:
        try:
            bibliotecas = self.biblioteca_crud.obtener_bibliotecas()

            if not bibliotecas:
                messagebox.showinfo("Bibliotecas", "No hay bibliotecas registradas.")
                return None

            mensaje = "--- BIBLIOTECAS DISPONIBLES ---\n"
            for i, biblioteca in enumerate(bibliotecas, 1):
                mensaje += (
                    f"{i}. ID: {biblioteca.id_biblioteca}\n"
                    f"   Nombre: {biblioteca.nombre}\n\n"
                )

            messagebox.showinfo("Bibliotecas", mensaje)

            seleccion = simpledialog.askinteger(
                "Seleccionar Biblioteca",
                f"Ingrese el número de la biblioteca (1-{len(bibliotecas)}):"
            )

            if seleccion is None:
                return None
            if seleccion < 1 or seleccion > len(bibliotecas):
                messagebox.showerror("Error", "Número inválido de biblioteca seleccionado.")
                return None

            return cast(Biblioteca, bibliotecas[seleccion - 1])

        except Exception as e:
            messagebox.showerror("Error", f"Error al seleccionar biblioteca: {e}")
            return None
    
#-------------------------------------------------------
# MENU CLIENTE
#-------------------------------------------------------
    """
        Muestra el menú de gestión de clientes.

        Permite realizar operaciones CRUD sobre cliente:
            1. Crear cliente.
            2. Listar clientes.
            3. Buscar cliente por id.
            4. buscar cliente por nombre
            5. Buscar por tipo de cliente
            6. Buscar por detalle del tipo de cliente
            7. Buscar clientes por vetados
            8. Actualizar cliente
            9. Actualizar tipo de cliente
            10. Actualizar detalle de tipo de cliente
            11. Actualizar vetado
            12. Eliminar cliente

        Returns:
            None
    """
    def mostrar_menu_cliente(self) -> None:
        if not self.sede_actual:
            messagebox.showerror("Error", "Debe seleccionar una sede primero")
            return

        id_sede = self.sede_actual.id_sede  
        biblioteca = self.biblioteca_crud.obtener_biblioteca_por_sede(id_sede)

        if not biblioteca:
            messagebox.showerror("Error", "No se encontró la biblioteca asociada a esta sede")
            return

        id_biblioteca = biblioteca.id_biblioteca
        
        while True:
            menu_texto = (
                "\n" + "-" * 30 + "\n"
                "   GESTION DE CLIENTES\n"
                f"Biblioteca: {self.biblioteca_actual.nombre}\n"
                + "-" * 30 + "\n"
                "1. Crear Cliente\n"
                "2. Listar Clientes\n"
                "3. Buscar cliente por Código\n"
                "4. Buscar clientes por nombre\n"
                "5. Buscar por tipo de cliente\n"
                "6. Buscar por detalle del tipo de cliente\n"
                "7. Buscar clientes por vetados\n"
                "8. Actualizar cliente\n"
                "9. Actualizar tipo de cliente\n"
                "10. Actualizar detalle de tipo de cliente\n"
                "11. Actualizar vetado\n"
                "12. Eliminar cliente\n"
                "0. Volver al menú principal"
            )

            messagebox.showinfo("Menú cliente", menu_texto)

            opcion = simpledialog.askstring("Menú Clientes", "Ingrese el número de la opción:")
            if opcion is None or opcion == "0":
                messagebox.showinfo("Salir", "Volviendo al menú principal")
                break

            match opcion.strip():
                case "1":
                    self.crear_cliente(id_biblioteca)
                case "2":
                    self.listar_clientes(id_biblioteca)
                case "3":
                    self.buscar_cliente_por_id(id_biblioteca)
                case "4":
                   self.buscar_clientes_por_nombre(id_biblioteca)
                case "5":
                    self.buscar_clientes_por_tipo(id_biblioteca)
                case "6":
                    self.buscar_clientes_por_detalle_tipo(id_biblioteca)
                case "7":
                    self.buscar_clientes_por_vetados(id_biblioteca)
                case "8":
                    self.actualizar_cliente(id_biblioteca)
                case "9":
                    self.actualizar_tipo_cliente(id_biblioteca)
                case "10":
                    self.actualizar_detalle_tipo_cliente(id_biblioteca)
                case "11":
                    self.actualizar_vetado_cliente(id_biblioteca)
                case "12":
                    self.eliminar_cliente(id_biblioteca)
                case _:
                    messagebox.showerror("Error", "Opción no válida. Intente nuevamente.")

    
    def crear_cliente(self, id_biblioteca: UUID) -> None:
        """crea un cliente nuevo.
        se le pide al usuario ingresar los atributos establecidos en la entidad cliente para crear el nuevo usuario
        returns none"""
        try:
            messagebox.showinfo("Crear Cliente", "--- CREAR CLIENTE ---")

            nombre = simpledialog.askstring("Crear Cliente", "Nombre del Cliente:")
            if nombre is None: return

            tipo_cliente = simpledialog.askstring("Crear Cliente", "Tipo del Cliente:")
            if tipo_cliente is None: return

            detalle_tipo = simpledialog.askstring("Crear Cliente", "Detalle del tipo de Cliente:")
            if detalle_tipo is None: return 

            cliente = self.cliente_crud.crear_cliente(
                nombre=nombre.strip().lower(),
                tipo_cliente=tipo_cliente.strip().lower(),
                detalle_tipo=detalle_tipo.strip().lower(),
                id_biblioteca=id_biblioteca,
                id_usuario_crea=self.usuario_actual.id_usuario if self.usuario_actual else None
            )
            messagebox.showinfo("Éxito", ("Cliente creado exitosamente:\n\n"
                                        f"ID: {cliente.codigo}\n"
                                        f"Nombre: {cliente.nombre}\n"
                                        f"Tipo: {cliente.tipo_cliente}\n"
                                        f"Detalle: {cliente.detalle_tipo}"
                )
            )

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")
            
    """lista todos los clientes que hayan en el sistema: los lista dependiendo de la sede que escojas"""
    def listar_clientes(self, id_biblioteca: UUID) -> None:
        try:
            clientes = self.cliente_crud.obtener_clientes(id_biblioteca)

            if not clientes:
                messagebox.showinfo("Clientes ", "No hay clientes registrados en está biblioteca.")
                return

            mensaje = f"--- CLIENTES ({len(clientes)}) ---\n\n"
            for i, cliente in enumerate(clientes, 1):
                mensaje += (
                    f"{i}. Código: {cliente.codigo}\n"
                    f"     Nombre: {(cliente.nombre or '').capitalize()}\n"
                    f"     Tipo de cliente: {(cliente.tipo_cliente or '').capitalize()}\n"
                    f"     Detalle: {(cliente.detalle_tipo or '').capitalize()}\n"
                    f"     Vetado: {'Sí' if cliente.vetado else 'No'}\n\n"
                )

            messagebox.showinfo("Clientes", mensaje)

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")


    
    def buscar_cliente_por_id(self, id_biblioteca: UUID) -> None:
        """para buscar un cliente por id, se le pide al usuario ingresar el id de dicho usuario, si existe lo muestra en pantalla
        y si no saca error de que no existe
        returns none"""
        try:
            cliente = self.seleccionar_cliente(id_biblioteca=id_biblioteca)
            if not cliente:
                messagebox.showerror("Error", "No se seleccionó ningún cliente o no hay clientes en esta biblioteca.")
                return
            
            mensaje = (
                "EXITO: Cliente encontrado:\n"
                f"ID: {cliente.codigo}\n"
                f"Nombre: {(cliente.nombre or '').title()}\n"
                f"Tipo de cliente: {(cliente.tipo_cliente or '').title()}\n"
                f"Detalle: {(cliente.detalle_tipo or '').title()}\n"
                f"Vetado: {'Sí' if cliente.vetado else 'No'}"
            )
            messagebox.showinfo("Cliente encontrado", mensaje)

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def buscar_clientes_por_nombre(self, id_biblioteca: UUID) -> None:
        """para buscar un cliente por nombre, se le pide al usuario ingresar el nombre de dicho usuario, si existe lo muestra en pantalla
        y si no saca error de que no existe
        returns none"""
        try:
            nombre = simpledialog.askstring("Buscar cliente", "Ingrese el nombre a buscar:")
            if nombre is None: return

            nombre = nombre.strip().lower()

            clientes = self.cliente_crud.obtener_clientes_por_nombre(nombre, id_biblioteca)

            if clientes:
                mensaje = f"--- CLIENTES CON NOMBRE '{nombre.upper()}' ({len(clientes)}) ---\n\n"
                for i, cliente in enumerate(clientes, 1):
                    mensaje += (
                        f"{i}. Código: {cliente.codigo}\n"
                        f"     Nombre: {(cliente.nombre or '').capitalize()}\n"
                        f"     Tipo de cliente: {(cliente.tipo_cliente or '').capitalize()}\n"
                        f"     Detalle: {(cliente.detalle_tipo or '').capitalize()}\n"
                        f"     Vetado: {'Sí' if cliente.vetado else 'No'}\n\n"
                    )
                messagebox.showinfo("Clientes encontrados", mensaje)
            else:
                messagebox.showerror("Error", f"No se encontraron clientes con nombre '{nombre}'.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def buscar_clientes_por_tipo(self, id_biblioteca: UUID) -> None:
        """para buscar un cliente por el tipo de usuario, se le pide al usuario ingresar el tipo de usuario de dicho usuario, 
        si existe lo muestra en pantalla y si no saca error de que no existe
        returns none"""
        try:
            tipo_cliente = simpledialog.askstring("Buscar cliente", "Ingrese el tipo del cliente a buscar:")
            if tipo_cliente is None: return

            tipo_cliente = tipo_cliente.strip().lower()

            clientes = self.cliente_crud.obtener_clientes_por_tipo_cliente(tipo_cliente, id_biblioteca)

            if clientes:
                mensaje = f"--- CLIENTES TIPO {tipo_cliente.upper()} ({len(clientes)}) ---\n\n"
                for i, cliente in enumerate(clientes, 1):
                    mensaje += (
                        f"{i}. Código: {cliente.codigo}\n"
                        f"     Nombre: {(cliente.nombre or '').capitalize()}\n"
                        f"     Tipo de cliente: {(cliente.tipo_cliente or '').capitalize()}\n"
                        f"     Detalle: {(cliente.detalle_tipo or '').capitalize()}\n"
                        f"     Vetado: {'Sí' if cliente.vetado else 'No'}\n\n"
                    )
                messagebox.showinfo("Clientes encontrados", mensaje)
            else:
                messagebox.showerror("Error", f"No se encontraron clientes de tipo '{tipo_cliente}'.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def buscar_clientes_por_detalle_tipo(self, id_biblioteca: UUID) -> None:
        try:
            detalle_tipo = simpledialog.askstring("Buscar cliente", "Ingrese el detalle del tipo de cliente a buscar:")
            if detalle_tipo is None: return

            detalle_tipo = detalle_tipo.strip().lower()

            clientes = self.cliente_crud.obtener_clientes_por_detalle_tipo(detalle_tipo, id_biblioteca)

            if clientes:
                mensaje = f"--- CLIENTES CON DETALLE {detalle_tipo.upper()} ({len(clientes)}) ---\n\n"
                for i, cliente in enumerate(clientes, 1):
                    mensaje += (
                        f"{i}. Código: {cliente.codigo}\n"
                        f"     Nombre: {(cliente.nombre or '').capitalize()}\n"
                        f"     Tipo de cliente: {(cliente.tipo_cliente or '').capitalize()}\n"
                        f"     Detalle: {(cliente.detalle_tipo or '').capitalize()}\n"
                        f"     Vetado: {'Sí' if cliente.vetado else 'No'}\n\n"
                    )
                messagebox.showinfo("Clientes encontrados", mensaje)
            else:
                messagebox.showerror("Error", f"No se encontraron clientes con detalle '{detalle_tipo}'.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def buscar_clientes_por_vetados(self, id_biblioteca: UUID) -> None:
        """para buscar un cliente por si es vetado o no, se le pide al usuario ingresar si el usuario es vetado o no,
        si existe lo muestra en pantalla y si no saca error de que no existe
        returns none"""
        try:
            vetado = messagebox.askyesno("Buscar cliente", "¿Desea buscar clientes vetados?")
           
            clientes = self.cliente_crud.obtener_clientes_por_vetado(vetado, id_biblioteca)

            if clientes:
                if vetado:
                    estado = "SÍ"
                else:
                    estado = "NO"

                mensaje = f"--- CLIENTES VETADOS = {estado} ({len(clientes)}) ---\n\n"
                for i, cliente in enumerate(clientes, 1):
                    mensaje += (
                        f"{i}. ID: {cliente.codigo}\n"
                        f"     Nombre: {(cliente.nombre or '').capitalize()}\n"
                        f"     Tipo de cliente: {(cliente.tipo_cliente or '').capitalize()}\n"
                        f"     Detalle: {(cliente.detalle_tipo or '').capitalize()}\n\n"
                    )
                messagebox.showinfo("Cliente encontrado", mensaje)
            else:
                estado = "SÍ" if vetado else "NO"
                messagebox.showinfo("Sin resultados", f"No se encontraron clientes vetados = {estado}.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def actualizar_cliente(self, id_biblioteca: UUID) -> None:
        """para actulizar un cliente primero se busca el cliente por id, se le pide al usuario ingresar el id de dicho usuario, 
        si existe se le pide al cliente ingresar el parametro a actualizar y si no existe saca error de que no existe
        returns none"""
        try:
            cliente = self.seleccionar_cliente(id_biblioteca)
            if not cliente:
                return
            
            messagebox.showinfo("Actualizar Cliente", f"Actualizando Cliente: {cliente.nombre}\n\nDeje en blanco para mantener el valor actual.")

            nuevo_nombre = simpledialog.askstring("Actualizar Cliente", f"Nombre actual ({cliente.nombre}):") or ""
            nuevo_tipo_cliente = simpledialog.askstring("Actualizar Cliente", f"Tipo de cliente actual ({cliente.tipo_cliente}):") or ""
            nuevo_detalle_tipo = simpledialog.askstring("Actualizar Cliente", f"Detalle actual ({cliente.detalle_tipo}):") or ""
            nuevo_vetado = messagebox.askyesno("Actualizar Cliente",
                                                f"El cliente actualmente está vetado: {'Sí' if cliente.vetado else 'No'}\n"
                                                "¿Desea marcarlo como vetado?")

            cambios = {}
            if nuevo_nombre.strip().lower():
                cambios["nombre"] = nuevo_nombre.strip().lower()
            if nuevo_tipo_cliente.strip().lower():
                cambios["tipo_cliente"] = nuevo_tipo_cliente.strip().lower()
            if nuevo_detalle_tipo.strip().lower():
                cambios["detalle_tipo"] = nuevo_detalle_tipo.strip().lower()
            if nuevo_vetado != cliente.vetado:
                cambios["vetado"] = nuevo_vetado


            if cambios:
                cliente_actualizado = self.cliente_crud.actualizar_cliente(cliente.codigo, id_biblioteca, **cambios)
                mensaje = ("Cliente actualizado\n\n"
                    f"ID: {cliente_actualizado.codigo}\n"
                    f"Nombre: {cliente_actualizado.nombre}\n"
                    f"Tipo: {cliente_actualizado.tipo_cliente}\n"
                    f"Detalle: {cliente_actualizado.detalle_tipo}\n"
                    f"Vetado: {'Sí' if cliente_actualizado.vetado else 'No'}"
                )
                messagebox.showinfo("Cliente actualizado", mensaje)
            else:
                messagebox.showinfo("Sin cambios", "No se realizaron modificaciones.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

    def actualizar_tipo_cliente(self, id_biblioteca: UUID) -> None:
        """para actulizar el tipo de un cliente primero se busca el cliente por id, se le pide al usuario ingresar el id de dicho usuario, 
        si existe se le pide al cliente ingresar el tipo de cliente a actualizar y si no existe saca error de que no existe
        returns none"""
        try:
            cliente = self.seleccionar_cliente(id_biblioteca)
            if not cliente:
                return
            
            messagebox.showinfo("Actualizar Tipo de cliente", f"Tipo de cliente actual del cliente {cliente.codigo}: {cliente.tipo_cliente}\n\nDeje en blanco para mantener el valor actual.")
            
            nuevo_tipo_cliente = simpledialog.askstring("Actualizar Tipo de cliente", f"Tipo actual ({cliente.tipo_cliente}):") or ""
            nuevo_tipo_cliente = nuevo_tipo_cliente.strip().lower()

            if nuevo_tipo_cliente:
                tipo_cliente_actualizado = self.cliente_crud.actualizar_tipo_cliente(cliente.codigo, nuevo_tipo_cliente, id_biblioteca)
                messagebox.showinfo("Éxito", f"Tipo de cliente actualizado:\n{tipo_cliente_actualizado}")
            else:
                messagebox.showinfo("Sin cambios", "No se realizaron modificaciones.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

    def actualizar_detalle_tipo_cliente(self, id_biblioteca: UUID) -> None:
        """para actulizar el detalle del tipo de un cliente primero se busca el cliente por id, se le pide al usuario ingresar el id de dicho usuario, 
        si existe se le pide al cliente ingresar el detalle del tipo a actualizar y si no existe saca error de que no existe
        returns none"""
        try:
            cliente = self.seleccionar_cliente(id_biblioteca)
            if not cliente:
                return

            messagebox.showinfo("Actualizar detalle de tipo", f"Detalle actual del cliente {cliente.codigo}: {cliente.detalle_tipo}\n\nDeje en blanco para mantener el valor actual.")

            nuevo_detalle_tipo = simpledialog.askstring("Actualizar detalle de tipo", f"Detalle actual ({cliente.detalle_tipo}):") or ""
            nuevo_detalle_tipo = nuevo_detalle_tipo.strip().lower()

            if nuevo_detalle_tipo:
                detalle_actualizado = self.cliente_crud.actualizar_detalle_tipo(cliente.codigo, nuevo_detalle_tipo, id_biblioteca)
                messagebox.showinfo("Éxito", f"Detalle de tipo actualizado:\n{detalle_actualizado}")
            else:
                messagebox.showinfo("Sin cambios", "No se realizaron modificaciones.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")
    
    def actualizar_vetado_cliente(self, id_biblioteca: UUID) -> None:
        """para actulizar el vetado de un cliente primero se busca el cliente por id, se le pide al usuario ingresar el id de dicho usuario, 
        si existe se le pide al cliente ingresar el vetado a actualizar y si no existe saca error de que no existe
        returns none"""
        try:
            cliente = self.seleccionar_cliente(id_biblioteca)
            if not cliente:
                return

            nuevo_vetado = messagebox.askyesno("Actualizar vetado", f"Cliente {cliente.codigo}: {cliente.nombre}\n\n¿Desea marcarlo como vetado?")

            if nuevo_vetado != cliente.vetado:
                self.cliente_crud.actualizar_vetado(cliente.codigo, nuevo_vetado, id_biblioteca)
                estado = "Sí" if nuevo_vetado else "No"
                messagebox.showinfo("Éxito", f"Estado de vetado actualizado a {estado}.")
            else:
                messagebox.showinfo("Sin cambios", "No se realizaron modificaciones.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")
    
    def eliminar_cliente(self, id_biblioteca: UUID) -> None:
        """para eliminar un cliente primero se busca el cliente por id, se le pide al usuario ingresar el id de dicho usuario, 
        si existe se le pregunta al usuario si esta seguro de eliminar al cliente y si no existe saca error de que no existe
        returns none"""
        try:
            cliente = self.seleccionar_cliente(id_biblioteca)
            if not cliente:
                return

            confirmacion = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar al cliente {cliente.nombre}?"
            )

            if confirmacion:
                if self.cliente_crud.eliminar_cliente(cliente.codigo, id_biblioteca):
                    messagebox.showinfo("Éxito", "Cliente eliminado exitosamente.")
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el cliente.")
            else:
                messagebox.showinfo("Cancelado", "Operación cancelada.")

        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")


#-------------------------------------------------------
# MENU CATEGORIA
#-------------------------------------------------------
    """ Muestra el menú de gestión de categorias.
    Permite realizar operaciones CRUD sobre cliente:
    1. Crear Categoria
    2. Listar Categorias
    3. Buscar categoria por nombre
    4. Actualizar categoria
    5. Eliminar categoria
    """
    def mostrar_menu_categoria(self) -> None:
        if not self.sede_actual:
            messagebox.showerror("Error", "Debe seleccionar una sede primero")
            return

        id_sede = self.sede_actual.id_sede  
        biblioteca = self.biblioteca_crud.obtener_biblioteca_por_sede(id_sede)

        if not biblioteca:
            messagebox.showerror("Error", "No se encontró la biblioteca asociada a esta sede")
            return

        id_biblioteca = biblioteca.id_biblioteca

        while True:
            menu_texto = (
                "\n" + "-" * 30 + "\n"
                "   GESTION DE CATEGORIAS\n"
                f"Biblioteca: {self.biblioteca_actual.nombre}\n"
                + "-" * 30 + "\n"
                "1. Crear Categoria\n"
                "2. Listar Categorias\n"
                "3. Buscar categoria por nombre\n"
                "4. Actualizar categoria\n"
                "5. Eliminar categoria\n"
                "0. Volver al menú principal"
            )

            messagebox.showinfo("Menú categoria", menu_texto)

            opcion = simpledialog.askstring("Menú categorias", "Ingrese el número de la opción:")
            if opcion is None or opcion == "0":
                messagebox.showinfo("Salir", "Volviendo al menú principal")
                break

            match opcion.strip():
                case "1":
                    self.crear_categoria(id_biblioteca)
                case "2":
                    self.listar_categorias(id_biblioteca)
                case "3":
                    self.buscar_categoria_por_nombre(id_biblioteca)
                case "4":
                    self.actualizar_categoria(id_biblioteca)
                case "5":
                    self.eliminar_categoria(id_biblioteca)
                case _:
                    messagebox.showerror("Error", "Opción no válida. Intente nuevamente.")

    def crear_categoria(self, id_biblioteca: UUID) -> None:
        """se le pide al usuario ingresar los atributos establecidos en la entidad categoria para crear la nueva categoria
        returns none"""
        try:
            messagebox.showinfo("Crear Categoria", "--- CREAR CATEGORIA ---")

            nombre = simpledialog.askstring("Crear Categoria", "Nombre de la Categoria:")
            if nombre is None: return
            nombre = nombre.strip().lower()

            descripcion = simpledialog.askstring("Crear categoria", "Descripcion de la categoría:")
            if descripcion is None: return
            descripcion = descripcion.strip().lower()

            categoria = self.categoria_crud.crear_categoria(
                id_biblioteca=id_biblioteca,
                nombre=nombre,
                descripcion=descripcion,
                id_usuario_crea=self.usuario_actual.id_usuario if self.usuario_actual else None
            )
            messagebox.showinfo("Éxito", ("Categoria creada exitosamente:\n\n"
                                        f"ID: {categoria.id_categoria}\n"
                                        f"Nombre: {categoria.nombre}\n"
                                        f"Descripción: {categoria.descripcion}\n"
                )
            )

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")
            
    def listar_categorias(self, id_biblioteca: UUID) -> None:
        """lista todas las categorias que hayan en el sistema"""
        try:
            categorias = self.categoria_crud.obtener_categorias(id_biblioteca=id_biblioteca)
            if not categorias:
                messagebox.showinfo("Categorias", "No hay categorias registrados.")
                return

            mensaje = f"--- CATEGORÍAS ({len(categorias)}) ---\n"
            for i, categoria in enumerate(categorias, 1):
                descripcion = categoria.descripcion if categoria.descripcion else "Sin descripción"
                mensaje += (
                    f"{i}. ID: {categoria.id_categoria}\n"
                    f"     Nombre: {categoria.nombre}\n"
                    f"     Descripción: {descripcion}\n"
                )

            messagebox.showinfo("Categorias ", mensaje)

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def buscar_categoria_por_nombre(self, id_biblioteca: UUID) -> None:
        """para buscar una categoria por el nombre se le pide al usuario ingresar el nombre de dicha categoria,
        si existe se muestra en pantalla la respuesta y si no sale error
        returns none"""
        try:
            nombre = simpledialog.askstring("Buscar Categoria", "Ingrese el nombre a buscar:")
            if nombre is None: return
            nombre = nombre.strip()

            categoria = self.categoria_crud.obtener_categoria_por_nombre(nombre, id_biblioteca=id_biblioteca)

            if categoria:
                descripcion = categoria.descripcion if categoria.descripcion else "Sin descripción"
                mensaje = (
                    "EXITO: Categoria encontrada:\n"
                    f"ID: {categoria.id_categoria}\n"
                    f"Nombre: {categoria.nombre}\n"
                    f"Descripcion: {descripcion}\n"
                )
                messagebox.showinfo("Categoria encontrada", mensaje)
            else:
                messagebox.showerror("Error", "Categoría no encontrada en esta biblioteca.")


        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def actualizar_categoria(self, id_biblioteca: UUID) -> None:
        """para actualizar una categoria se le pide al usuario ingresar el nombre de dicha categoria,
        si existe se le pide al usuario ingresar el nuevo nombre o descripcion a actualizar y si no existe sale error.
        returns none"""
        try:
            nombre = simpledialog.askstring("Actualizar Categoria", "Ingrese el nombre de la categoria a actualizar:")
            if nombre is None: return
            nombre = nombre.strip()

            categoria = self.categoria_crud.obtener_categoria_por_nombre(nombre, id_biblioteca=id_biblioteca)

            if not categoria:
                messagebox.showerror("Error", "Categoria no encontrada.")
                return

            messagebox.showinfo("Actualizar Categoria", f"Actualizando Categoria: {categoria.nombre}\n\nDeje en blanco para mantener el valor actual.")

            nuevo_nombre = simpledialog.askstring("Actualizar Categoria", f"Nombre actual ({categoria.nombre}):") or ""
            nueva_descripcion = simpledialog.askstring("Actualizar Categoria", f"Descripcion actual ({categoria.descripcion}):") or ""

            cambios = {}
            if nuevo_nombre.strip().lower():
                cambios["nombre"] = nuevo_nombre.strip().lower()
            if nueva_descripcion.strip().lower():
                cambios["descripcion"] = nueva_descripcion.strip().lower()

            if cambios:
                categoria_actualizada = self.categoria_crud.actualizar_categoria(id_categoria=categoria.id_categoria, id_biblioteca=id_biblioteca, **cambios)
                mensaje = ("Categoría actualizada:\n\n"
                    f"ID: {categoria_actualizada.id_categoria}\n"
                    f"Nombre: {categoria_actualizada.nombre}\n"
                    f"Descripción: {categoria_actualizada.descripcion}"
                )
                messagebox.showinfo("Categoría actualizada", mensaje)
            else:
                messagebox.showinfo("Sin cambios", "No se realizaron modificaciones.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

    def eliminar_categoria(self, id_biblioteca: UUID) -> None:
        """para eliminar una categoria se le pide al usuario ingresar el nombre de la categoria, si esta existe 
        le aparecera un mensaje de confirmacion de eliminacion en pantalla para que el usuario decida si eliminarla o no.
        si no existe la categoria sale error.
        returns none"""
        try:
            nombre = simpledialog.askstring("Eliminar Categoria", "Ingrese el nombre de la categoria a eliminar:")
            if nombre is None:  
                return
            nombre = nombre.strip()

            categoria = self.categoria_crud.obtener_categoria_por_nombre(nombre, id_biblioteca=id_biblioteca)

            if not categoria:
                messagebox.showerror("Error", "Categoria no encontrada.")
                return

            confirmacion = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar la categoría {categoria.id_categoria}: {categoria.nombre}?"
            )

            if confirmacion:
                if self.categoria_crud.eliminar_categoria(id_categoria=categoria.id_categoria, id_biblioteca=id_biblioteca):
                    messagebox.showinfo("Éxito", "Categoria eliminada exitosamente.")
                else:
                    messagebox.showerror("Error", "No se pudo eliminar la categoria.")
            else:
                messagebox.showinfo("Cancelado", "Operación cancelada.")

        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")


#-------------------------------------------------------
# MENU MATERIAL
#-------------------------------------------------------

    def mostrar_menu_material(self) -> None:
        """
        Muestra el menú de gestión de materiales bibliográficos.
        Permite realizar operaciones CRUD sobre materiales:
        1. Crear material.
        2. Listar materiales.
        3. Buscar material por ID.
        4. Buscar material por título.
        5. Actualizar material.
        6. Eliminar material.
        0. Volver al menú principal.
        Returns:
            None"""
        if not self.sede_actual:
            messagebox.showerror("Error", "Debe seleccionar una sede primero")
            return

        id_sede = self.sede_actual.id_sede  
        biblioteca = self.biblioteca_crud.obtener_biblioteca_por_sede(id_sede)

        if not biblioteca:
            messagebox.showerror("Error", "No se encontró la biblioteca asociada a esta sede")
            return

        id_biblioteca = biblioteca.id_biblioteca

        while True:
            menu_texto = (
                "\n" + "-" * 30 + "\n"
                "   GESTION DE MATERIALES\n"
                + "-" * 30 + "\n"
                "1. Crear Material\n"
                "2. Listar Materiales\n"
                "3. Buscar materiales por ID\n"
                "4. Buscar materiales por titulo\n"
                "5. Buscar materiales por autor\n"
                "6. Buscar material por estado\n"
                "7. Buscar por categoria (id de la categoria)\n"
                "8. Actualizar material\n"
                "9. Actualizar estado por material\n"
                "10. Eliminar material\n"
                "0. Volver al menú principal"
            )

            messagebox.showinfo("Menú Materiales", menu_texto)

            opcion = simpledialog.askstring("Menú Materiales", "Ingrese el número de la opción:")
            if opcion is None or opcion == "0":
                messagebox.showinfo("Salir", "Volviendo al menú principal")
                break

            match opcion.strip():
                case "1":
                    self.crear_material(id_biblioteca)
                case "2":
                    self.listar_materiales(id_biblioteca)
                case "3":
                    self.buscar_material_por_id(id_biblioteca)
                case "4":
                   self.buscar_materiales_por_titulo(id_biblioteca)
                case "5":
                    self.buscar_materiales_por_autor(id_biblioteca)
                case "6":
                    self.buscar_materiales_por_estado(id_biblioteca)
                case "7":
                    self.buscar_material_por_categoria(id_biblioteca)
                case "8":
                   self.actualizar_material(id_biblioteca)
                case "9":
                    self.actualizar_estado_material(id_biblioteca)
                case "10":
                    self.eliminar_material(id_biblioteca)
                case _:
                    messagebox.showerror("Error", "Opción no válida. Intente nuevamente.")

    def crear_material(self, id_biblioteca: UUID) -> None:
        """Crea un nuevo material bibliográfico.
        Se solicita al usuario ingresar los atributos del material y se guarda
        en la base de datos.
        Returns None"""
        try:
            messagebox.showinfo("Crear Material", "--- CREAR MATERIAL ---")

            titulo = simpledialog.askstring("Crear Material", "Título del material:")
            if titulo is None: 
                return
            titulo = titulo.strip().lower()
            if not titulo:
                messagebox.showerror("Error", "El título es obligatorio")
                return
            if len(titulo) > 80:
                messagebox.showerror("Error", "El título no puede exceder 80 caracteres")
                return

            autor = simpledialog.askstring("Crear Material", "Autor del material:")
            if autor is None: 
                return
            autor = autor.strip().lower()
            if not autor:
                messagebox.showerror("Error", "El autor es obligatorio")
                return
            if len(autor) > 80:
                messagebox.showerror("Error", "El autor no puede exceder 80 caracteres")
                return

            categoria = self.seleccionar_categoria(id_biblioteca)
            if not categoria:
                return 
            id_categoria = categoria.id_categoria

            material = self.material_crud.crear_material(
                id_biblioteca=id_biblioteca,
                titulo=titulo,
                autor=autor,
                estado="disponible",
                id_sede=self.sede_actual.id_sede,
                id_categoria=id_categoria,
                id_usuario_crea=self.usuario_actual.id_usuario if self.usuario_actual else None
            )
            messagebox.showinfo("Éxito", ("Material creado exitosamente:\n\n"
                                        f"ID: {material.id_biblioteca}\n"
                                        f"Titulo: {material.titulo}\n"
                                        f"Autor: {material.autor}\n"
                                        f"Estado: {material.estado}\n"
                )
            )


        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")
            
    def listar_materiales(self, id_biblioteca: UUID) -> None:
        """Lista todos los materiales bibliográficos de la biblioteca seleccionada.
        Muestra título, autor, estado y otros datos relevantes.
        Returns None"""

        try:
            materiales = self.material_crud.obtener_materiales(id_biblioteca)

            if not materiales:
                messagebox.showinfo("Materiales ", "No hay materiales registrados.")
                return

            mensaje = f"--- MATERIALES BIBLIOGRAFICOS ({len(materiales)}) ---\n"
            for i, material in enumerate(materiales, 1):
                biblioteca = cast(Biblioteca, material.biblioteca)
                categoria = cast(Categoria, material.categoria)

                mensaje += (
                    f"{i}. ID: {material.id_material}\n"
                    f"     Titulo: {(material.titulo or '').capitalize()}\n"
                    f"     Autor: {(material.autor or '').capitalize()}\n"
                    f"     Estado: {(material.estado or '').capitalize()}\n"
                    f"     Biblioteca: {biblioteca.nombre}\n"
                    f"     Categoría: {categoria.nombre}\n\n"
                )

            messagebox.showinfo("Materiales  ", mensaje)

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def buscar_material_por_id(self, id_biblioteca: UUID) -> None:
        """Busca un material por su identificador único.
        Se solicita el ID y, si existe, se muestra la información completa.
        Returns None"""

        try:
            material = self.seleccionar_material(id_biblioteca)
            if not material:
                return

            biblioteca = cast(Biblioteca, material.biblioteca)
            categoria = cast(Categoria, material.categoria)
            mensaje = (
                    "EXITO: Material BIbliográfico encontrado:\n"
                    f"ID: {material.id_material}\n"
                    f"Titulo: {(material.titulo or '').capitalize()}\n"
                    f"Autor: {(material.autor or '').capitalize()}\n"
                    f"Estado: {(material.estado or '').capitalize()}\n"
                    f"Biblioteca: {biblioteca.nombre}\n"
                    f"Categoría: {categoria.nombre}\n\n"
            )
            messagebox.showinfo("Material encontrado", mensaje)

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
    
    def buscar_materiales_por_titulo(self, id_biblioteca: UUID) -> None:
        """Busca un material bibliográfico por título.
        Se solicita el nombre y, si existe, se muestra en pantalla.
        Returns None"""

        try:
            titulo = simpledialog.askstring("Buscar Material", "Ingrese el titulo a buscar:")
            if titulo is None:  
                return
            titulo =  titulo.strip().lower()

            materiales = self.material_crud.obtener_materiales_por_titulo(titulo, id_biblioteca)

            if materiales:
                mensaje = f"--- MATERIALES CON TITULO '{titulo.upper()}' ({len(materiales)}) ---\n\n"
                for i, material in enumerate(materiales, 1):
                    biblioteca = cast(Biblioteca, material.biblioteca)
                    categoria = cast(Categoria, material.categoria)

                    mensaje += (
                        "EXITO: Material BIbliográfico encontrado:\n"
                        f"{i}. ID: {material.id_material})\n"
                        f"     Titulo: {(material.titulo or '').capitalize()}\n"
                        f"     Autor: {(material.autor or '').capitalize()}\n"
                        f"     Estado: {(material.estado or '').capitalize()}\n"
                        f"     Biblioteca: {biblioteca.nombre}\n"
                        f"     Categoría: {categoria.nombre}\n\n"
                    )
                messagebox.showinfo("Material encontrado", mensaje)
            else:
                messagebox.showerror("Error", f"No se encontraron Materiales con titulo '{titulo}'.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def buscar_materiales_por_autor(self, id_biblioteca: UUID) -> None:
        """Busca un material bibliográfico por autor.
        Se solicita el nombre y, si existe, se muestra en pantalla.
        Returns None"""
        try:
            autor = simpledialog.askstring("Buscar material", "Ingrese el autor del material a buscar:")
            if autor is None:  
                return
            autor = autor.strip().lower()

            materiales = self.material_crud.obtener_materiales_por_autor(autor, id_biblioteca)

            if materiales:
                mensaje = f"--- MATERIALES CON AUTOR '{autor.upper()}' ({len(materiales)}) ---\n\n"
                for i, material in enumerate(materiales, 1):
                    biblioteca = cast(Biblioteca, material.biblioteca)
                    categoria = cast(Categoria, material.categoria)

                    mensaje += (
                        "EXITO: Material BIbliográfico encontrado:\n"
                        f"{i}. ID: {material.id_material})\n"
                        f"     Titulo: {(material.titulo or '').capitalize()}\n"
                        f"     Autor: {(material.autor or '').capitalize()}\n"
                        f"     Estado: {(material.estado or '').capitalize()}\n"
                        f"     Biblioteca: {biblioteca.nombre}\n"
                        f"     Categoría: {categoria.nombre}\n\n"
                    )
                messagebox.showinfo("Material encontrado", mensaje)
            else:
                messagebox.showerror("Error", f"No se encontraron Materiales con autor '{autor}'.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def buscar_materiales_por_estado(self, id_biblioteca: UUID) -> None:
        """Busca un material bibliográfico por estado.
        Se solicita el estado del material y, si existe, se muestra en pantalla.
        Returns None"""
        try:
            estado = simpledialog.askstring("Buscar Materiales", "Ingrese el estado del material a buscar:")
            if estado is None:  
                return
            estado = estado.strip().lower()

            materiales = self.material_crud.obtener_materiales_por_estado(estado, id_biblioteca)
            
            if materiales:
                mensaje = f"--- MATERIALES CON ESTADO '{estado.upper()}' ({len(materiales)}) ---\n\n"
                for i, material in enumerate(materiales, 1):
                    biblioteca = cast(Biblioteca, material.biblioteca)
                    categoria = cast(Categoria, material.categoria)

                    mensaje += (
                        "EXITO: Material encontrado:\n"
                        f"{i}. ID: {material.id_material})\n"
                        f"     Titulo: {(material.titulo or '').capitalize()}\n"
                        f"     Autor: {(material.autor or '').capitalize()}\n"
                        f"     Estado: {(material.estado or '').capitalize()}\n"
                        f"     Biblioteca: {biblioteca.nombre}\n"
                        f"     Categoría: {categoria.nombre}\n\n"
                    )
                messagebox.showinfo("Material encontrado", mensaje)
            else:
                messagebox.showerror("Error", f"No se encontraron Materiales con estado '{estado}'.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def buscar_material_por_categoria(self, id_biblioteca: UUID) -> None:
        """Busca un material bibliográfico por categoria.
        Se solicita la categoria del material y, si existe, se muestra en pantalla.
        Returns None"""
        try:
            categoria = self.seleccionar_categoria(id_biblioteca)
            if not categoria:
                return

            materiales = self.material_crud.obtener_materiales_por_categoria(categoria.id_categoria, id_biblioteca)

            if materiales:
                mensaje = f"--- MATERIALES DE LA CATEGORÍA {categoria.nombre} ({len(materiales)}) ---\n\n"
                for i, material in enumerate(materiales, 1):
                    biblioteca = cast(Biblioteca, material.biblioteca)
                    categoria = cast(Categoria, material.categoria)

                    mensaje += (
                        f"{i}. ID: {material.id_material}\n"
                        f"     Titulo: {(material.titulo or '').capitalize()}\n"
                        f"     Autor: {(material.autor or '').capitalize()}\n"
                        f"     Estado: {(material.estado or '').capitalize()}\n"
                        f"     Biblioteca: {biblioteca.nombre}\n"
                        f"     Categoría: {categoria.nombre}\n\n"
                    )
                messagebox.showinfo("Materiales encontrados", mensaje)
            else:
                messagebox.showerror("Error", "No se encontraron materiales para esta categoría.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def actualizar_material(self, id_biblioteca: UUID) -> None:
        """Actualiza los datos de un material existente.
        Se pide el ID o título del material, luego se permite modificar
        atributos como título, autor, estado o descripción.
        Returns None"""

        try:
            material = self.seleccionar_material(id_biblioteca)
            if not material:
                return
            
            messagebox.showinfo("Actualizar Material", f"Actualizando Material: {(material.titulo or '').capitalize()}\n\nDeje en blanco para mantener el valor actual.")

            cambios = {}

            nuevo_titulo = simpledialog.askstring("Actualizar Material", f"Título actual ({material.titulo}):") or ""
            nuevo_autor = simpledialog.askstring("Actualizar Material", f"Autor actual ({material.autor}):") or ""
            nuevo_estado = simpledialog.askstring("Actualizar Material", f"Estado actual ({material.estado}):") or ""

            if messagebox.askyesno("Actualizar Material", "¿Desea cambiar la categoría de este material?"):
                nueva_categoria = self.seleccionar_categoria(id_biblioteca)
                if nueva_categoria:
                    cambios["id_categoria"] = nueva_categoria.id_categoria

            if nuevo_titulo.strip():
                if len(nuevo_titulo.strip()) > 80:
                    raise ValueError("El título no puede exceder 80 caracteres")
                cambios["titulo"] = nuevo_titulo.strip()

            if nuevo_autor.strip():
                if len(nuevo_autor.strip()) > 80:
                    raise ValueError("El autor no puede exceder 80 caracteres")
                cambios["autor"] = nuevo_autor.strip()

            if nuevo_estado.strip():
                if len(nuevo_estado.strip()) > 80:
                    raise ValueError("El estado no puede exceder 80 caracteres")
                cambios["estado"] = nuevo_estado.strip()

            if cambios:
                material_actualizado = self.material_crud.actualizar_material(material.id_material, id_biblioteca=id_biblioteca, **cambios)
                biblioteca = cast(Biblioteca, material_actualizado.biblioteca)
                categoria = cast(Categoria, material_actualizado.categoria)
                
                mensaje = (
                    "Material actualizado exitosamente:\n\n"
                    f"ID: {material_actualizado.id_material}\n"
                    f"Título: {(material_actualizado.titulo or '').capitalize()}\n"
                    f"Autor: {(material_actualizado.autor or '').capitalize()}\n"
                    f"Estado: {(material_actualizado.estado or '').capitalize()}\n"
                    f"Categoría: {categoria.nombre}\n"
                    f"Biblioteca: {biblioteca.nombre}\n"
                )
                messagebox.showinfo("Éxito", mensaje)
            else:
                messagebox.showinfo("Sin cambios", "No se realizaron modificaciones.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

    def actualizar_estado_material(self, id_biblioteca: UUID) -> None:
        """Actualiza el estado de un material existente.
        Se pide el ID del material, luego se permite modificar el
        atributo estado.
        Returns None"""
        try:
            material = self.seleccionar_material(id_biblioteca)
            if not material:
                return

            messagebox.showinfo(
                "Actualizar Estado del Material", f"Estado actual del material '{material.titulo}': {(material.estado or '').capitalize()}\n\n""Deje en blanco para mantener el valor actual.")

            nuevo_estado = simpledialog.askstring("Actualizar Estado del Material", f"Estado actual ({material.estado or ''}):") or ""
            nuevo_estado = nuevo_estado.strip()

            if nuevo_estado:
                material_actualizado = self.material_crud.actualizar_estado(material.id_material, id_biblioteca=id_biblioteca, nuevo_estado=nuevo_estado)
                messagebox.showinfo(
                    "Éxito",
                    f"Estado actualizado del material:\n"
                    f"ID: {material_actualizado.id_material}\n"
                    f"Título: {(material_actualizado.titulo or '').capitalize()}\n"
                    f"Estado: {(material_actualizado.estado or '').capitalize()}\n"
                )
            else:
                messagebox.showinfo("Sin cambios", "No se realizaron modificaciones.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

    def eliminar_material(self, id_biblioteca: UUID) -> None:
        """Elimina un material bibliográfico.
        Se pide confirmación antes de borrar el registro de la base de datos.
        Returns None"""

        try:
            material = self.seleccionar_material(id_biblioteca)
            if not material:
                return

            confirmacion = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar el material '{material.titulo}'?"
            )

            if confirmacion:
                if self.material_crud.eliminar_material(material.id_material, id_biblioteca):
                    messagebox.showinfo("Éxito", "Material eliminado exitosamente.")
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el material.")
            else:
                messagebox.showinfo("Cancelado", "Operación cancelada.")

        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")


#-------------------------------------------------------
# MENU RESERVA
#-------------------------------------------------------

    def mostrar_menu_reserva(self) -> None:
        """
        Muestra el menú de gestión de reservas.

        Permite realizar operaciones CRUD sobre reservas:
        1. Crear reserva.
        2. Listar reservas.
        3. Buscar reserva por ID.
        4. Buscar reservas por fecha de la reserva
        5. Buscar preservas or estado de la reserva
        6. Buscar reservas por material (id del material)
        7. Buscar reservas por cliente (id del cliente)
        8. Actualizar reserva
        9. Actualizar estado
        10. Eliminar reserva
        0. Volver al menú principal.

        Returns:
        None"""
        if not self.sede_actual:
            messagebox.showerror("Error", "Debe seleccionar una sede primero")
            return

        id_sede = self.sede_actual.id_sede  
        biblioteca = self.biblioteca_crud.obtener_biblioteca_por_sede(id_sede)

        if not biblioteca:
            messagebox.showerror("Error", "No se encontró la biblioteca asociada a esta sede")
            return

        id_biblioteca = biblioteca.id_biblioteca

        while True:
            menu_texto = (
                "\n" + "-" * 30 + "\n"
                "   GESTION DE RESERVAS\n"
                + "-" * 30 + "\n"
                "1. Crear Reserva\n"
                "2. Listar Reservas\n"
                "3. Buscar reserva por ID\n"
                "4. Buscar reservas por fecha de la reserva\n"
                "5. Buscar preservas or estado de la reserva\n"
                "6. Buscar reservas por material (id del material)\n"
                "7. Buscar reservas por cliente (id del cliente)\n"
                "8. Actualizar reserva\n"
                "9. Actualizar estado\n"
                "10. Eliminar reserva\n"
                "0. Volver al menú principal"
            )

            messagebox.showinfo("Menú Reservas", menu_texto)

            opcion = simpledialog.askstring("Menú Reservas", "Ingrese el número de la opción:")
            if opcion is None or opcion == "0":
                messagebox.showinfo("Salir", "Volviendo al menú principal")
                break

            match opcion.strip():
                case "1":
                    self.crear_reserva(id_biblioteca)
                case "2":
                    self.obtener_reservas(id_biblioteca)
                case "3":
                    self.obtener_reserva(id_biblioteca)
                case "4":
                   self.obtener_reservas_por_fecha(id_biblioteca)
                case "5":
                    self.obtener_reservas_por_estado(id_biblioteca)
                case "6":
                    self.obtener_reserva_por_material(id_biblioteca)
                case "7":
                    self.obtener_reservas_por_cliente(id_biblioteca)
                case "8":
                   self.actualizar_reserva(id_biblioteca)
                case "9":
                    self.actualizar_estado(id_biblioteca)
                case "10":
                    self.eliminar_reserva(id_biblioteca)
                case _:
                    messagebox.showerror("Error", "Opción no válida. Intente nuevamente.")

    def crear_reserva(self, id_biblioteca: UUID) -> None:
        """Crea una nueva reserva de material.
        Solicita al usuario seleccionar cliente y material, y registra la reserva.
        Returns None"""

        try:
            messagebox.showinfo("Crear Reserva", "--- CREAR RESERVA ---")

            material = self.seleccionar_material(id_biblioteca)
            if not material:
                return

            cliente = self.seleccionar_cliente(id_biblioteca)
            if not cliente:
                return

            material = self.material_crud.obtener_material(material.id_material, id_biblioteca)
            if not material:
                messagebox.showerror("Error", f"No se encontró el material con ID {material.id_material}.")
                return
            if material.estado != "disponible":
                messagebox.showerror("Error", f"El material '{material.titulo}' no está disponible (estado actual: {material.estado}).")
                return

            reserva = self.reserva_crud.crear_reserva(
                fecha_reserva=date.today(),
                estado="activa",
                id_material=material.id_material,
                cod_cliente=cliente.codigo,
                id_biblioteca=id_biblioteca,
                id_usuario_crea=self.usuario_actual.id_usuario if self.usuario_actual else None
            )

            self.material_crud.actualizar_estado(material.id_material, id_biblioteca, "reservado")

            messagebox.showinfo(
                "Éxito", 
                f"Reserva creada exitosamente:\n\n"
                f"ID: {reserva.id_reserva}\n"
                f"Material: {material.titulo}\n"
                f"Cliente: {cliente.nombre}\n"
                f"Estado: {reserva.estado}\n\n"
                f"El material '{material.titulo}' ahora está en estado 'reservado'."
            )

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def obtener_reservas(self, id_biblioteca: UUID) -> None:
        """Lista todas las reservas registradas en la biblioteca seleccionada.
        Muestra Id, estado, fecha de reserva, material y biblioteca
        Returns None"""
        try:
            reservas = self.reserva_crud.obtener_reservas(id_biblioteca)
            if not reservas:
                messagebox.showinfo("Reservas", "No hay reservas registradas.")
                return

            mensaje = f"--- RESERVAS ({len(reservas)}) ---\n"
            for i, reserva in enumerate(reservas, 1):
                material = cast(Material_Bibliografico, reserva.material)
                biblioteca = cast(Biblioteca, reserva.biblioteca)

                mensaje += (
                    f"{i}. ID: {reserva.id_reserva}\n"
                    f"     Fecha de reserva: {reserva.fecha_reserva}\n"
                    f"     Estado: {reserva.estado}\n"
                    f"     Material: {material.titulo}\n"
                    f"     Biblioteca: {biblioteca.nombre}\n\n"
                )

            messagebox.showinfo("Reservas", mensaje)

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def obtener_reserva(self, id_biblioteca: UUID) -> None:
        """Busca una reserva mediante su identificador único.
        Se solicita el ID y se muestran los datos si existe.
        Returns None"""

        try:
            reserva = self.seleccionar_reserva(id_biblioteca)
            if not reserva:
                return
            
            cliente = cast(Cliente, reserva.cliente)
            material = cast(Material_Bibliografico, reserva.material)
            biblioteca = cast(Biblioteca, reserva.biblioteca)

            mensaje = ("EXITO: Reserva encontrada:\n\n"
                f"ID: {reserva.id_reserva}\n"
                f"Fecha de reserva: {reserva.fecha_reserva}\n"
                f"Estado:  {reserva.estado}\n"
                f"Cliente: {cliente.nombre}\n"
                f"Material: {material.titulo}\n"
                f"Biblioteca: {biblioteca.nombre}\n"
            )
            messagebox.showinfo("Reserva encontrada", mensaje)

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def obtener_reservas_por_fecha(self, id_biblioteca: UUID) -> None:
        """Busca una reserva mediante su fecha de reserva .
        Se solicita la fecha de la reserva y se muestran los datos si existe.
        Returns None"""
        try:
            fecha_str = simpledialog.askstring("Buscar Reserva", "Ingrese la fecha de la reserva a buscar (YYYY-MM-DD): ")
            if fecha_str is None: return

            try:
                fecha = date.fromisoformat(fecha_str)
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD.")
                return
            
            reservas = self.reserva_crud.obtener_reservas_por_fecha(fecha, id_biblioteca)

            if reservas:
                mensaje = f"--- RESERVAS EN {fecha} ({len(reservas)}) ---\n\n"
                for i, reserva in enumerate(reservas, 1):
                    cliente = cast(Cliente, reserva.cliente)
                    material = cast(Material_Bibliografico, reserva.material)
                    biblioteca = cast(Biblioteca, reserva.biblioteca)

                    mensaje += (
                    f"{i}. ID: {reserva.id_reserva}\n"
                    f"     Fecha de reserva: {reserva.fecha_reserva}\n"
                    f"     Estado:  {reserva.estado}\n"
                    f"     Cliente: {cliente.nombre}\n"
                    f"     Material: {material.titulo}\n"
                    f"     Biblioteca: {biblioteca.nombre}\n\n"
                    )
                messagebox.showinfo("Reserva encontrada", mensaje)
            else:
                messagebox.showerror("Error", f"No se encontraron reservas con fecha {fecha}.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}") 
        
    def obtener_reservas_por_estado(self, id_biblioteca: UUID) -> None:
        """Busca una reserva mediante su estado.
        Se solicita el esatdo de la reserva y se muestran los datos si existe.
        Returns None"""
        try:
            estado = simpledialog.askstring("Buscar Reserva", "Ingrese el estado de la reserva a buscar: ")
            if estado is None: return

            estado = estado.strip().lower()
            reservas = self.reserva_crud.obtener_reservas_por_estado(estado, id_biblioteca)

            if reservas:
                mensaje = f"--- RESERVAS EN ESTADO {estado.upper()} ({len(reservas)}) ---\n\n"
                for i, reserva in enumerate(reservas, 1):
                    cliente = cast(Cliente, reserva.cliente)
                    material = cast(Material_Bibliografico, reserva.material)
                    biblioteca = cast(Biblioteca, reserva.biblioteca)

                    mensaje += ("EXITO: Reserva encontrada:\n\n"
                    f"{i}. ID: {reserva.id_reserva}\n"
                    f"     Fecha de reserva: {reserva.fecha_reserva}\n"
                    f"     Estado:  {reserva.estado}\n"
                    f"     Cliente: {cliente.nombre}\n"
                    f"     Material: {material.titulo}\n"
                    f"     Biblioteca: {biblioteca.nombre}\n\n"
                    )
                messagebox.showinfo("Reserva encontrada", mensaje)
            else:
                messagebox.showerror("Error", f"No se encontraron reservas en estado {estado}.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}") 

    def obtener_reserva_por_material(self, id_biblioteca: UUID) -> None:
        """Busca una reserva mediante el material.
        Se solicita el material reservadoy se muestran los datos si existe.
        Returns None"""
        try:
            material = self.seleccionar_material(id_biblioteca)
            if not material:
                return

            reserva = self.reserva_crud.obtener_reserva_por_material(material.id_material, id_biblioteca)
            if not reserva:
                messagebox.showerror("Error", f"No hay reservas activas para el material '{material.titulo}'.")
                return
        
            cliente = cast(Cliente, reserva.cliente)
            biblioteca = cast(Biblioteca, reserva.biblioteca)

            mensaje = ("EXITO: Reserva encontrada:\n\n"
                f"ID: {reserva.id_reserva}\n"
                f"Fecha de reserva: {reserva.fecha_reserva}\n"
                f"Estado:  {reserva.estado}\n"
                f"Cliente: {cliente.nombre}\n"
                f"Material: {material.titulo}\n"
                f"Biblioteca: {biblioteca.nombre}\n\n"
            )
            messagebox.showinfo("Reserva encontrada", mensaje)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}") 

    def obtener_reservas_por_cliente(self, id_biblioteca: UUID) -> None:
        """Busca una reserva mediante su cliente reservador.
        Se le solicita al usuario escoger el cliente mediante una lista de clientes y se muestran los datos si existe.
        Returns None"""
        try:
            cliente = self.seleccionar_cliente(id_biblioteca)
            if not cliente:
                return

            reservas = self.reserva_crud.obtener_reservas_por_cliente(cliente.codigo, id_biblioteca)

            if reservas:
                mensaje = f"--- RESERVAS DEL CLIENTE {cliente.codigo} ({len(reservas)}) ---\n\n"
                for i, reserva in enumerate(reservas, 1):
                    cliente = cast(Cliente, reserva.cliente)
                    material = cast(Material_Bibliografico, reserva.material)
                    biblioteca = cast(Biblioteca, reserva.biblioteca)

                    mensaje += ("EXITO: Reserva encontrada:\n\n"
                    f"{i}. ID: {reserva.id_reserva}\n"
                    f"     Fecha de reserva: {reserva.fecha_reserva}\n"
                    f"     Estado:  {reserva.estado}\n"
                    f"     Cliente: {cliente.nombre}\n"
                    f"     Material: {material.titulo}\n"
                    f"     Biblioteca: {biblioteca.nombre}\n\n"
                    )
                messagebox.showinfo("Reserva encontrada", mensaje)
            else:
                messagebox.showerror("Error", f"No se encontraron reservas del cliente {cliente.codigo}.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def actualizar_reserva(self, id_biblioteca: UUID) -> None:
        """Actualiza la información de una reserva existente.
        Permite modificar estado, fecha o material reservado.
        Returns None"""

        try:
            reserva = self.seleccionar_reserva(id_biblioteca)
            if not reserva:
                return

            messagebox.showinfo("Actualizar Reserva", f"Actualizando reserva {reserva.id_reserva}\n\nDeje en blanco para mantener el valor actual.")

            # Inicializamos cambios ANTES de usarlo
            cambios = {}

            nueva_fecha = simpledialog.askstring("Actualizar Reserva", f"Fecha actual ({reserva.fecha_reserva}) [YYYY-MM-DD]:") or ""

            nuevo_estado = simpledialog.askstring("Actualizar Reserva", f"Estado actual ({reserva.estado}):") or ""

            if messagebox.askyesno("Actualizar Reserva", "¿Desea cambiar el cliente de esta reserva?"):
                nuevo_cliente = self.seleccionar_cliente(id_biblioteca)
                if nuevo_cliente:
                    cambios["id_cliente"] = nuevo_cliente.id_cliente  # 👈 Ajusta al nombre real de tu modelo

            if messagebox.askyesno("Actualizar Reserva", "¿Desea cambiar el material de esta reserva?"):
                nuevo_material = self.seleccionar_material(id_biblioteca)
                if nuevo_material:
                    cambios["id_material"] = nuevo_material.id_material

            if nueva_fecha.strip():
                try:
                    cambios["fecha_reserva"] = date.fromisoformat(nueva_fecha.strip())
                except ValueError:
                    messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD.")
                    return
                    
            if nuevo_estado.strip():
                cambios["estado"] = nuevo_estado.strip().lower()

            if cambios:
                reserva_actualizada = self.reserva_crud.actualizar_reserva(reserva.id_reserva, id_biblioteca, **cambios)

                cliente = cast(Cliente, reserva_actualizada.cliente)
                material = cast(Material_Bibliografico, reserva_actualizada.material)
                biblioteca = cast(Biblioteca, reserva_actualizada.biblioteca)

                mensaje = (
                    f"ID Reserva: {reserva_actualizada.id_reserva}\n"
                    f"Fecha de reserva: {reserva_actualizada.fecha_reserva}\n"
                    f"Estado: {reserva_actualizada.estado}\n"
                    f"Cliente: {cliente.nombre}\n"
                    f"Material: {material.titulo}\n"
                    f"Biblioteca: {biblioteca.nombre}\n"
                )
                messagebox.showinfo("Éxito", mensaje)
            else:
                messagebox.showinfo("Sin cambios", "No se realizaron modificaciones.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

    def actualizar_estado(self, id_biblioteca: UUID) -> None:
        """Actualiza el esstado de una reserva existente.
        Permite modificar el estado de la reserva.
        Returns None"""
        try:
            reserva = self.seleccionar_reserva(id_biblioteca)
            if not reserva:
                return

            messagebox.showinfo("Actualizar Estado", f"Estado actual de la reserva {reserva.id_reserva}: {reserva.estado}\n\n""Deje en blanco si no desea modificar.")

            nuevo_estado = simpledialog.askstring("Actualizar Estado", f"Nuevo estado (actual: {reserva.estado}):") or ""

            if nuevo_estado.strip():
                reserva_actualizada = self.reserva_crud.actualizar_estado(reserva.id_reserva, id_biblioteca=id_biblioteca, nuevo_estado=nuevo_estado.strip().lower())
                messagebox.showinfo("Éxito", f"Estado actualizado:\n{reserva_actualizada}")
            else:
                messagebox.showinfo("Sin cambios", "No se realizaron modificaciones.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

    def eliminar_reserva(self, id_biblioteca: UUID) -> None:
        """Elimina una reserva de la base de datos.
        Solicita confirmación antes de proceder.
        Returns None"""

        try:
            reserva = self.seleccionar_reserva(id_biblioteca)
            if not reserva:
                return

            confirmacion = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar la reserva ID {reserva.id_reserva}?\n"
                f"Material: {reserva.id_material}\nCliente: {reserva.cod_cliente}"
            )

            if confirmacion:
                if self.reserva_crud.eliminar_reserva(reserva.id_reserva, id_biblioteca=id_biblioteca):
                    self.material_crud.actualizar_estado(reserva.id_material, id_biblioteca=id_biblioteca, nuevo_estado="disponible")
                    material = cast(Material_Bibliografico, reserva.material)
                    messagebox.showinfo(
                        "Éxito",
                        f"La reserva ID {reserva.id_reserva} fue eliminada exitosamente.\n"
                        f"El material '{material.titulo}' ahora está disponible."
                    )
                else:
                    messagebox.showerror("Error", "No se pudo eliminar la reserva.")
            else:
                messagebox.showinfo("Cancelado", "Operación cancelada.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")


#-------------------------------------------------------
# MENU PRESTAMO
#-------------------------------------------------------

    def mostrar_menu_prestamo(self) -> None:
        """Muestra el menú de gestión de préstamos.

        Permite realizar operaciones CRUD sobre préstamos:
        1. Crear préstamo.
        2. Listar préstamos.
        3. Buscar préstamo por ID.
        4. Buscar prestamo por fecha del prestamo
        5. Buscar prestamo por fecha de entrega
        6. Buscar prestamo por material (id del material)
        7. Buscar prestamo por cliente (id del cliente)
        8. Actualizar prestamo
        9. Actualizar fecha de entrega
        10. Eliminar prestamo
        0. Volver al menú principal.

        Returns:
        None"""

        if not self.sede_actual:
            messagebox.showerror("Error", "Debe seleccionar una sede primero")
            return

        id_sede = self.sede_actual.id_sede  
        biblioteca = self.biblioteca_crud.obtener_biblioteca_por_sede(id_sede)

        if not biblioteca:
            messagebox.showerror("Error", "No se encontró la biblioteca asociada a esta sede")
            return

        id_biblioteca = biblioteca.id_biblioteca

        while True:
            menu_texto = (
                "\n" + "-" * 30 + "\n"
                "   GESTION DE PRESTAMOS\n"
                + "-" * 30 + "\n"
                "1. Crear Prestamo\n"
                "2. Listar Prestamos\n"
                "3. Buscar prestamo por ID\n"
                "4. Buscar prestamo por fecha del prestamo\n"
                "5. Buscar prestamo por fecha de entrega\n"
                "6. Buscar prestamo por material (id del material)\n"
                "7. Buscar prestamo por cliente (id del cliente)\n"
                "8. Actualizar prestamo\n"
                "9. Actualizar fecha de entrega\n"
                "10. Eliminar prestamo\n"
                "0. Volver al menú principal"
            )

            messagebox.showinfo("Menú Prestamos", menu_texto)

            opcion = simpledialog.askstring("Menú Prestamos", "Ingrese el número de la opción:")
            if opcion is None or opcion == "0":
                messagebox.showinfo("Salir", "Volviendo al menú principal")
                break

            match opcion.strip():
                case "1":
                    self.crear_prestamo(id_biblioteca)
                case "2":
                    self.obtener_prestamos(id_biblioteca)
                case "3":
                    self.obtener_prestamo(id_biblioteca)
                case "4":
                   self.obtener_prestamos_por_fecha_prestamo(id_biblioteca)
                case "5":
                    self.obtener_prestamos_por_fecha_entrega(id_biblioteca)
                case "6":
                    self.obtener_prestamo_por_material(id_biblioteca)
                case "7":
                    self.obtener_prestamos_por_cliente(id_biblioteca)
                case "8":
                   self.actualizar_prestamo(id_biblioteca)
                case "9":
                    self.actualizar_fecha_entrega(id_biblioteca)
                case "10":
                    self.eliminar_prestamo(id_biblioteca)
                case _:
                    messagebox.showerror("Error", "Opción no válida. Intente nuevamente.")

    def crear_prestamo(self, id_biblioteca: UUID) -> None:
        """Crea un nuevo préstamo de material.
        Solicita cliente, material y fechas de préstamo/entrega.
        Returns None"""

        try:
            messagebox.showinfo("Crear Préstamo", "--- CREAR PRÉSTAMO ---")

            material = self.seleccionar_material(id_biblioteca)
            if not material:
                return

            cliente = self.seleccionar_cliente(id_biblioteca)
            if not cliente:
                return

            if material.estado != "disponible":
                messagebox.showerror("Error", f"El material '{material.titulo}' no está disponible (estado actual: {material.estado}).")
                return

            fecha_prestamo = date.today()
            fecha_entrega = fecha_prestamo + timedelta(days=7)

            prestamo = self.prestamo_crud.crear_prestamo(
                fecha_prestamo=date.today(),
                fecha_entrega=fecha_entrega,
                id_material=material.id_material,
                cod_cliente=cliente.codigo,
                id_biblioteca=id_biblioteca,
                id_usuario_crea=self.usuario_actual.id_usuario if self.usuario_actual else None
            )

            self.material_crud.actualizar_estado(material.id_material, id_biblioteca, "prestado")

            messagebox.showinfo(
                "Éxito", 
                f"Préstamo creado exitosamente:\n\n"
                f"ID: {prestamo.id}\n"
                f"Material: {material.titulo}\n"
                f"Cliente: {cliente.nombre}\n"
                f"Fecha de entrega: {prestamo.fecha_entrega}\n\n"
                f"El material '{material.titulo}' ahora está en estado 'prestado'."
            )

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def obtener_prestamos(self, id_biblioteca: UUID) -> None:
        """Lista todos los préstamos registrados en la biblioteca seleccionada.
        Muestra cliente, material, fechas y estado.
        Returns None"""

        try:
            prestamos = self.prestamo_crud.obtener_prestamos(id_biblioteca)
            if not prestamos:
                messagebox.showinfo("Préstamos", "No hay préstamos registrados.")
                return

            mensaje = f"--- PRÉSTAMOS ({len(prestamos)}) ---\n"
            for i, prestamo in enumerate(prestamos, 1):
                cliente = cast(Cliente, prestamo.cliente)
                material = cast(Material_Bibliografico, prestamo.material)
                biblioteca = cast(Biblioteca, prestamo.biblioteca)

                mensaje += (
                    f"{i}. ID: {prestamo.id}\n"
                    f"   Fecha préstamo: {prestamo.fecha_prestamo}\n"
                    f"   Fecha entrega:  {prestamo.fecha_entrega}\n"
                    f"   Cliente: {cliente.nombre}\n"
                    f"   Material: {material.titulo}\n"
                    f"   Biblioteca: {biblioteca.nombre}\n\n"
                )

            messagebox.showinfo("Préstamos", mensaje)

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def obtener_prestamo(self, id_biblioteca: UUID) -> None:
        """Busca un prestamo mediante su ID.
        Se le solicita al usuario escoger el prestamo mediante una lista de prestamos y se muestran los datos si existe.
        Returns None"""
        try:
            prestamo = self.seleccionar_prestamo(id_biblioteca)
            if not prestamo:
                return  

            cliente = cast(Cliente, prestamo.cliente)
            material = cast(Material_Bibliografico, prestamo.material)
            biblioteca = cast(Biblioteca, prestamo.biblioteca)

            mensaje = ("EXITO: Préstamo encontrado:\n\n"
                f"ID: {prestamo.id}\n"
                f"Fecha de préstamo: {prestamo.fecha_prestamo}\n"
                f"Fecha de entrega:  {prestamo.fecha_entrega}\n"
                f"Cliente: {cliente.nombre}\n"
                f"Material: {material.titulo}\n"
                f"Biblioteca: {biblioteca.nombre}\n"
            )
            messagebox.showinfo("Préstamo encontrado", mensaje)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}") 

    def obtener_prestamos_por_fecha_prestamo(self, id_biblioteca: UUID) -> None:
        """Busca un prestamo mediante su fecha de prestamo.
        Se le solicita al usuario escoger el prestamo mediante una lista de prestamos y se muestran los datos si existe.
        Returns None"""
        try:
            fecha_str = simpledialog.askstring("Buscar Préstamo", "Ingrese la fecha del préstamo a buscar (YYYY-MM-DD): ")
            if fecha_str is None: return

            try:
                fecha = date.fromisoformat(fecha_str)
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD.")
                return
            
            prestamos = self.prestamo_crud.obtener_prestamos_por_fecha_prestamo(fecha, id_biblioteca)

            if prestamos:
                mensaje = f"--- PRÉSTAMOS EN {fecha} ({len(prestamos)}) ---\n\n"
                for i, prestamo in enumerate(prestamos, 1):
                    cliente = cast(Cliente, prestamo.cliente)
                    material = cast(Material_Bibliografico, prestamo.material)
                    biblioteca = cast(Biblioteca, prestamo.biblioteca)

                    mensaje += (
                    f"{i}. ID: {prestamo.id}\n"
                    f"     Fecha de préstamo: {prestamo.fecha_prestamo}\n"
                    f"     Fecha de entrega:  {prestamo.fecha_entrega}\n"
                    f"     Cliente: {cliente.nombre}\n"
                    f"     Material: {material.titulo}\n"
                    f"     Biblioteca: {biblioteca.nombre}\n"
                    )
                messagebox.showinfo("Préstamo encontrado", mensaje)
            else:
                messagebox.showerror("Error", f"No se encontraron préstamos con fecha {fecha}.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}") 

    def obtener_prestamos_por_fecha_entrega(self, id_biblioteca: UUID) -> None:
        """Busca un prestamo mediante su fecha de entrega.
        Se le solicita al usuario escoger el prestamo mediante una lista de prestamos y se muestran los datos si existe.
        Returns None"""
        try:
            fecha_str = simpledialog.askstring("Buscar Préstamo", "Ingrese la fecha de entrega del préstamo a buscar (YYYY-MM-DD): ")
            if fecha_str is None: return

            try:
                fecha = date.fromisoformat(fecha_str)
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD.")
                return
            
            prestamos = self.prestamo_crud.obtener_prestamos_por_fecha_entrega(fecha, id_biblioteca)

            if prestamos:
                mensaje = f"--- PRÉSTAMOS CON ENTREGA {fecha} ({len(prestamos)}) ---\n\n"
                for i, prestamo in enumerate(prestamos, 1):
                    cliente = cast(Cliente, prestamo.cliente)
                    material = cast(Material_Bibliografico, prestamo.material)
                    biblioteca = cast(Biblioteca, prestamo.biblioteca)

                    mensaje += (
                    f"{i}. ID: {prestamo.id}\n"
                    f"     Fecha de préstamo: {prestamo.fecha_prestamo}\n"
                    f"     Fecha de entrega:  {prestamo.fecha_entrega}\n"
                    f"     Cliente: {cliente.nombre}\n"
                    f"     Material: {material.titulo}\n"
                    f"     Biblioteca: {biblioteca.nombre}\n\n"
                    )
                messagebox.showinfo("Préstamo encontrado", mensaje)
            else:
                messagebox.showerror("Error", f"No se encontraron préstamos con fecha de entrega {fecha}.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}") 
        
    def obtener_prestamo_por_material(self, id_biblioteca: UUID) -> None:
        """Busca un prestamo mediante el material prestado.
        Se le solicita al usuario escoger el prestamo mediante una lista de prestamos y se muestran los datos si existe.
        Returns None"""
        try:
            material = self.seleccionar_material(id_biblioteca)
            if not material:
                return

            prestamo = self.prestamo_crud.obtener_prestamo_por_material(material.id_material, id_biblioteca)
            if not prestamo:
                messagebox.showerror("Error", f"No hay préstamo activo para el material '{material.titulo}'.")
                return

            cliente = cast(Cliente, prestamo.cliente)
            biblioteca = cast(Biblioteca, prestamo.biblioteca)
            mensaje = ("EXITO: Préstamo encontrado:\n\n"
                f"ID: {prestamo.id}\n"
                f"Fecha de préstamo: {prestamo.fecha_prestamo}\n"
                f"Fecha de entrega:  {prestamo.fecha_entrega}\n"
                f"Cliente: {cliente.nombre}\n"
                f"Material: {material.titulo}\n"
                f"Biblioteca: {biblioteca.nombre}\n"
            )
            messagebox.showinfo("Préstamo encontrado", mensaje)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}") 
        
    def obtener_prestamos_por_cliente(self, id_biblioteca: UUID) -> None:
        """Busca un prestamo mediante su cliente prestador.
        Se le solicita al usuario escoger el prestamo mediante una lista de clientes con prestamos y se muestran los datos si existe.
        Returns None"""
        try:
            cliente = self.seleccionar_cliente(id_biblioteca)
            if not cliente:
                return

            prestamos = self.prestamo_crud.obtener_prestamos_por_cliente(cliente.codigo, id_biblioteca)
            if not prestamos:
                messagebox.showwarning("Sin resultados", f"No hay préstamos activos para el cliente '{cliente.nombre}'.")
                return

            if prestamos:
                mensaje = f"--- PRÉSTAMOS DEL CLIENTE {cliente.nombre} ({len(prestamos)}) ---\n\n"
                for i, prestamo in enumerate(prestamos, 1):
                    material = cast(Material_Bibliografico, prestamo.material)
                    biblioteca = cast(Biblioteca, prestamo.biblioteca)

                    mensaje += ("EXITO: Préstamo encontrado:\n\n"
                    f"{i}. ID: {prestamo.id}\n"
                    f"     Fecha de préstamo: {prestamo.fecha_prestamo}\n"
                    f"     Fecha de entrega:  {prestamo.fecha_entrega}\n"
                    f"     Cliente: {cliente.nombre}\n"
                    f"     Material: {material.titulo}\n"
                    f"     Biblioteca: {biblioteca.nombre}\n"
                    )
                messagebox.showinfo("Préstamo encontrado", mensaje)
            else:
                messagebox.showerror("Error", f"No se encontraron préstamos del cliente {cliente.nombre}.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}") 

    def actualizar_prestamo(self, id_biblioteca: UUID) -> None:
        """Actualiza la información de un préstamo.
        Permite modificar fechas de entrega o estado del préstamo.
        Returns None"""

        try:
            prestamo = self.seleccionar_prestamo(id_biblioteca)
            if not prestamo:
                return  
            
            messagebox.showinfo("Actualizar Préstamo", f"Actualizando préstamo: {prestamo.id}\n\nDeje en blanco para mantener el valor actual.")

            cambios = {}

            nueva_fecha_prestamo = simpledialog.askstring("Actualizar Préstamo", f"Fecha de préstamo actual ({prestamo.fecha_prestamo}) [YYYY-MM-DD]:") or ""

            nueva_fecha_entrega = simpledialog.askstring("Actualizar Préstamo", f"Fecha de entrega actual ({prestamo.fecha_entrega}) [YYYY-MM-DD]:") or ""

            if messagebox.askyesno("Actualizar Préstamo", "¿Desea cambiar el cliente de este préstamo?"):
                nuevo_cliente = self.seleccionar_cliente(id_biblioteca)
                if nuevo_cliente:
                    cambios["id_cliente"] = nuevo_cliente.codigo

            if messagebox.askyesno("Actualizar Préstamo", "¿Desea cambiar el material de este préstamo?"):
                nuevo_material = self.seleccionar_material(id_biblioteca)
                if nuevo_material:
                    cambios["id_material"] = nuevo_material.id_material

            if nueva_fecha_prestamo.strip():
                try:
                    cambios["fecha_prestamo"] = date.fromisoformat(nueva_fecha_prestamo.strip())
                except ValueError:
                    messagebox.showerror("Error", "Formato de fecha de préstamo inválido. Use YYYY-MM-DD.")
                    return

            if nueva_fecha_entrega.strip():
                try:
                    cambios["fecha_entrega"] = date.fromisoformat(nueva_fecha_entrega.strip())
                except ValueError:
                    messagebox.showerror("Error", "Formato de fecha de entrega inválido. Use YYYY-MM-DD.")
                    return
            
            if cambios:
                prestamo_actualizado = self.prestamo_crud.actualizar_prestamo(prestamo.id, id_biblioteca=id_biblioteca, **cambios)

                cliente = cast(Cliente, prestamo_actualizado.cliente)
                material = cast(Material_Bibliografico, prestamo_actualizado.material)

                mensaje = (
                    "Préstamo actualizado exitosamente:\n\n"
                    f"ID Préstamo: {prestamo_actualizado.id}\n"
                    f"Fecha de préstamo: {prestamo_actualizado.fecha_prestamo}\n"
                    f"Fecha de entrega: {prestamo_actualizado.fecha_entrega}\n"
                    f"Cliente: {cliente.nombre}\n"
                    f"Material: {material.titulo}\n"
                )
                messagebox.showinfo("Éxito", mensaje)
            else:
                messagebox.showinfo("Sin cambios", "No se realizaron modificaciones.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

    def actualizar_fecha_entrega(self, id_biblioteca: UUID) -> None:
        """Actualiza la fecha de entrega de un préstamo.
        Permite modificar fechas de entrega de un prestamo.
        Returns None"""

        try:
            prestamo = self.seleccionar_prestamo(id_biblioteca)
            if not prestamo:
                return  

            messagebox.showinfo("Actualizar Fecha de Entrega", f"Préstamo ID {prestamo.id}\n\nFecha de entrega actual: {prestamo.fecha_entrega}\n\nDeje en blanco para mantener el valor actual.")

            nueva_fecha_entrega = simpledialog.askstring("Actualizar Fecha de Entrega", f"Fecha entrega actual ({prestamo.fecha_entrega}):") or ""

            if nueva_fecha_entrega.strip():
                try:
                    fecha_convertida = datetime.strptime(nueva_fecha_entrega.strip(), "%Y-%m-%d").date()
                except ValueError:
                    messagebox.showerror("Error", "Formato inválido. Use AAAA-MM-DD.")
                    return

                prestamo_actualizado = self.prestamo_crud.actualizar_prestamo(prestamo.id, id_biblioteca=id_biblioteca, fecha_entrega=fecha_convertida)
                messagebox.showinfo("Éxito", f"Fecha de entrega actualizada:\n{prestamo_actualizado}")
            else:
                messagebox.showinfo("Sin cambios", "No se realizaron modificaciones.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")
        
    def eliminar_prestamo(self, id_biblioteca: UUID) -> None:
        """Elimina un préstamo de la base de datos.
        Solicita confirmación antes de proceder.
        Returns None"""

        try:
            prestamo = self.seleccionar_prestamo(id_biblioteca)
            if not prestamo:
                return  
            
            confirmacion = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar al préstamo con ID {prestamo.id}?\n"
                f"Material: {prestamo.id_material}\nCliente: {prestamo.cod_cliente}"
            )

            if confirmacion:
                if self.prestamo_crud.eliminar_prestamo(prestamo.id, id_biblioteca=id_biblioteca):
                    self.material_crud.actualizar_estado(prestamo.id_material, id_biblioteca=id_biblioteca, nuevo_estado="disponible")
                    material = cast(Material_Bibliografico, prestamo.material)
                    messagebox.showinfo(
                        "Éxito",
                        f"El préstamo ID {prestamo.id} fue eliminada exitosamente.\n"
                        f"El material '{material.titulo}' ahora está disponible."
                    )
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el préstamo.")
            else:
                messagebox.showinfo("Cancelado", "Operación cancelada.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}") 



#-------------------------------------------------------
# MENU SANCION
#-------------------------------------------------------

    def mostrar_menu_sanciones(self) -> None:
        """Muestra el menú de gestión de sanciones.

        Permite realizar operaciones CRUD sobre sanciones:
        1. Crear sanción.
        2. Listar sanciones.
        3. Buscar sanción por ID.
        4. Buscar sancion por motivo
        5. Buscar sancion por fecha
        6. Buscar sancion por monto
        7. Buscar sancion por cliente (id del cliente)
        8. Actualizar sancion
        9. Eliminar sancion
        0. Volver al menú principal.

        Returns:
        None"""

        if not self.sede_actual:
            messagebox.showerror("Error", "Debe seleccionar una sede primero")
            return

        id_sede = self.sede_actual.id_sede  
        biblioteca = self.biblioteca_crud.obtener_biblioteca_por_sede(id_sede)

        if not biblioteca:
            messagebox.showerror("Error", "No se encontró la biblioteca asociada a esta sede")
            return

        id_biblioteca = biblioteca.id_biblioteca

        while True:
            menu_texto = (
                "\n" + "-" * 30 + "\n"
                "   GESTION DE SANCIONES\n"
                + "-" * 30 + "\n"
                "1. Crear Sancion\n"
                "2. Listar Sanciones\n"
                "3. Buscar sancion por ID\n"
                "4. Buscar sancion por motivo\n"
                "5. Buscar sancion por fecha\n"
                "6. Buscar sancion por monto\n"
                "7. Buscar sancion por cliente (id del cliente)\n"
                "8. Actualizar sancion\n"
                "9. Eliminar sancion\n"
                "0. Volver al menú principal"
            )

            messagebox.showinfo("Menú Sanciones", menu_texto)

            opcion = simpledialog.askstring("Menú Sanciones", "Ingrese el número de la opción:")
            if opcion is None or opcion == "0":
                messagebox.showinfo("Salir", "Volviendo al menú principal")
                break

            match opcion.strip():
                case "1":
                    self.crear_sancion(id_biblioteca)
                case "2":
                    self.obtener_sanciones(id_biblioteca)
                case "3":
                    self.obtener_sancion(id_biblioteca)
                case "4":
                    self.obtener_sanciones_por_motivo(id_biblioteca)
                case "5":
                    self.obtener_sanciones_por_fecha_sancion(id_biblioteca)
                case "6":
                    self.obtener_sanciones_por_monto(id_biblioteca)
                case "7":
                    self.obtener_sanciones_por_cliente(id_biblioteca)
                case "8":
                   self.actualizar_sancion(id_biblioteca)
                case "9":
                   self.eliminar_sancion(id_biblioteca)
                case _:
                    messagebox.showerror("Error", "Opción no válida. Intente nuevamente.")

    def crear_sancion(self, id_biblioteca: UUID) -> None:
        """Crea una nueva sanción para un cliente. 
        Solicita cliente, motivo y duración de la sanción.
        Returns None"""

        try:
            messagebox.showinfo("Crear Sanción", "--- CREAR SANCIÓN ---")

            motivo = simpledialog.askstring("Crear Sanción", "Ingrese el motivo de la sanción:")
            if motivo is None: return
            motivo = motivo.strip()
            if not motivo:
                messagebox.showerror("Error", "El motivo es obligatorio.")
                return

            monto = simpledialog.askfloat("Crear Sanción", "Ingrese el monto $ de la sanción:")
            if monto is None: return
            if monto <= 0:
                messagebox.showerror("Error", "El monto debe ser mayor que cero.")
                return

            cliente = self.seleccionar_cliente(id_biblioteca)
            if not cliente:
                return
            
            sancion = self.sancion_crud.crear_sancion(
                motivo = motivo,
                fecha_sancion= date.today(),
                monto= monto,
                cod_cliente= cliente.codigo,
                id_biblioteca=id_biblioteca,
                id_usuario_crea=self.usuario_actual.id_usuario if self.usuario_actual else None
            )

            self.cliente_crud.actualizar_vetado(cliente.codigo, True, id_biblioteca)

            messagebox.showinfo("Éxito", f"Sanción creada exitosamente:\n\n"
                                         f"ID: {sancion.id_sancion}\n"
                                         f"Fecha sanción: {sancion.fecha_sancion}\n"
                                         f"Motivo: '{sancion.motivo}'\n"
                                         f"Monto: ${sancion.monto}\n"
                                         f"Cliente: {cliente.nombre}\n\n"
                                         f"El cliente {cliente.nombre} (Código: {cliente.codigo}) ahora se encuentra vetado.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def obtener_sanciones(self, id_biblioteca: UUID) -> None:
        """Lista todas las sanciones registradas en la biblioteca seleccionada.
        Muestra cliente, motivo, estado y fechas.
        Returns None"""

        try:
            sanciones = self.sancion_crud.obtener_sanciones(id_biblioteca)
            if not sanciones:
                messagebox.showinfo("Sanciones", "No hay sanciones registradas.")
                return

            mensaje = "--- LISTA DE SANCIONES ---\n\n"
            for i, sancion in enumerate(sanciones, 1):
                cliente = cast(Cliente, sancion.cliente)
                biblioteca = cast(Biblioteca, sancion.biblioteca)

                mensaje += (f"{i}. ID: {sancion.id_sancion}\n"
                            f"   Motivo: {sancion.motivo}\n"
                            f"   Fecha: {sancion.fecha_sancion}\n"
                            f"   Monto: {sancion.monto}\n"
                            f"   Cliente: {cliente.nombre}\n"
                            f"   Biblioteca: {biblioteca.nombre}\n\n"
                )
            
            messagebox.showinfo("Sanciones", mensaje)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def obtener_sancion(self, id_biblioteca: UUID) -> None:
        """Busca una sancion mediante su ID.
        Se le solicita al usuario escoger la sancion mediante una lista de clientes sancionados y se muestran los datos si existe.
        Returns None"""

        try:
            sancion = self.seleccionar_sancion(id_biblioteca)
            if not sancion:
                return
            
            cliente = cast(Cliente, sancion.cliente)
            biblioteca = cast(Biblioteca, sancion.biblioteca)
            
            mensaje = (f"EXITO: Sanción encontrada: \n\n"
                        f"ID: {sancion.id_sancion}\n"
                        f"Motivo: {sancion.motivo}\n"
                        f"Fecha: {sancion.fecha_sancion}\n"
                        f"Monto: {sancion.monto}\n"
                        f"Cliente: {cliente.nombre}\n"
                        f"Biblioteca: {biblioteca.nombre}\n"
            )
            messagebox.showinfo("Sanción encontrada", mensaje)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def obtener_sanciones_por_motivo(self, id_biblioteca: UUID) -> None:
        """Busca una sancion mediante el motivo de la sancion.
        Se le solicita al usuario escoger la sancion mediante una lista de clientes sancionados y se muestran los datos si existe.
        Returns None"""
        try:
            motivo = simpledialog.askstring("Buscar Sanción", "Ingrese el motivo:")
            if motivo is None: return

            motivo = motivo.strip().lower()
            sanciones = self.sancion_crud.obtener_sanciones_por_motivo(motivo, id_biblioteca)

            if sanciones:
                mensaje = f"--- SANCIONES POR MOTIVO '{motivo.upper()}' ({len(sanciones)}) ---\n\n"
                for i, sancion in enumerate(sanciones, 1):
                    cliente = cast(Cliente, sancion.cliente)
                    biblioteca = cast(Biblioteca, sancion.biblioteca)

                    mensaje += (f"{i}. ID: {sancion.id_sancion}\n" 
                                f"     Fecha de la sanción: {sancion.fecha_sancion}\n"
                                f"     Monto: {sancion.monto}\n"
                                f"     Cliente: {cliente.nombre}\n"
                                f"     Biblioteca: {biblioteca.nombre}\n\n"
                                )
                messagebox.showinfo("Sanciones encontradas", mensaje)
            else:
                messagebox.showerror("Error", f"No se encontraron sanciones con motivo '{motivo}'.")

        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def obtener_sanciones_por_fecha_sancion(self, id_biblioteca: UUID) -> None:
        """Busca una sancion mediante su fecha de sancion.
        Se le solicita al usuario escoger la sancion mediante una lista de clientes sancionados y se muestran los datos si existe.
        Returns None"""
        try:
            fecha_str = simpledialog.askstring("Buscar Sanción", "Ingrese la fecha de sanción (YYYY-MM-DD):")
            if fecha_str is None: return

            try:
                fecha = date.fromisoformat(fecha_str)
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD.")
                return
            
            sanciones = self.sancion_crud.obtener_sanciones_por_fecha_sancion(fecha, id_biblioteca)

            if sanciones:
                mensaje = f"--- SANCIONES EN FECHA {fecha} ({len(sanciones)}) ---\n\n"
                for i, sancion in enumerate(sanciones, 1):
                    cliente = cast(Cliente, sancion.cliente)
                    biblioteca = cast(Biblioteca, sancion.biblioteca)

                    mensaje += (f"{i}. ID: {sancion.id_sancion}\n" 
                                f"     Fecha de la sanción: {sancion.fecha_sancion}\n"
                                f"     Monto: {sancion.monto}\n"
                                f"   Cliente: {cliente.nombre}\n"
                                f"   Biblioteca: {biblioteca.nombre}\n\n"
                                )
                messagebox.showinfo("Sanciones encontradas", mensaje)
            else:
                messagebox.showerror("Error", f"No se encontraron sanciones en la fecha {fecha}.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def obtener_sanciones_por_monto(self, id_biblioteca: UUID) -> None:
        """Busca una sancion mediante el monto de la sancion.
        Se le solicita al usuario escoger la sancion mediante una lista de clientes sancionados y se muestran los datos si existe.
        Returns None"""
        try:
            monto = simpledialog.askfloat("Buscar Sanción", "Ingrese el monto:")
            if monto is None: return

            sanciones = self.sancion_crud.obtener_sanciones_por_monto(monto, id_biblioteca)

            if sanciones:
                mensaje = f"--- SANCIONES CON MONTO {monto} ({len(sanciones)}) ---\n\n"
                for i, sancion in enumerate(sanciones, 1):
                    cliente = cast(Cliente, sancion.cliente)
                    biblioteca = cast(Biblioteca, sancion.biblioteca)

                    mensaje += (f"{i}. ID: {sancion.id_sancion}\n" 
                                f"     Fecha de la sanción: {sancion.fecha_sancion}\n"
                                f"     Monto: {sancion.monto}\n"
                                f"   Cliente: {cliente.nombre}\n"
                                f"   Biblioteca: {biblioteca.nombre}\n\n"
                                )
                messagebox.showinfo("Sanciones encontradas", mensaje)
            else:
                messagebox.showerror("Error", f"No se encontraron sanciones con monto {monto}.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def obtener_sanciones_por_cliente(self, id_biblioteca: UUID) -> None:
        """Busca una sancion mediante el cliente sancionado.
        Se le solicita al usuario escoger la sancion mediante una lista de clientes sancionados y se muestran los datos si existe.
        Returns None"""
        try:
            cliente = self.seleccionar_cliente(id_biblioteca)
            if not cliente:
                return

            sanciones = self.sancion_crud.obtener_sanciones_por_cliente(cliente.codigo, id_biblioteca)

            if sanciones:
                mensaje = f"--- SANCIONES DEL CLIENTE {cliente.nombre} ({len(sanciones)}) ---\n\n"
                for i, sancion in enumerate(sanciones, 1):
                    cliente = cast(Cliente, sancion.cliente)
                    biblioteca = cast(Biblioteca, sancion.biblioteca)

                    mensaje += (f"{i}. ID: {sancion.id_sancion}\n" 
                                f"     Fecha de la sanción: {sancion.fecha_sancion}\n"
                                f"     Monto: {sancion.monto}\n"
                                f"   Cliente: {cliente.nombre}\n"
                                f"   Biblioteca: {biblioteca.nombre}\n\n"
                                )
                messagebox.showinfo("Sanciones encontradas", mensaje)
            else:
                messagebox.showerror("Error", f"No se encontraron sanciones para el cliente {cliente.nombre}.")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")

    def actualizar_sancion(self, id_biblioteca: UUID) -> None:
        """Actualiza los datos de una sanción existente.
        Permite modificar motivo, estado o duración.
        Returns None"""

        try:
            sancion = self.seleccionar_sancion(id_biblioteca)
            if not sancion:
                return

            sancion = self.sancion_crud.obtener_sancion(sancion.id_sancion, id_biblioteca)
            if not sancion:
                messagebox.showerror("Error", "Sanción no encontrada.")
                return

            messagebox.showinfo("Actualizar Sanción", f"Actualizando sanción {sancion.id_sancion}\n\nDeje en blanco para mantener el valor actual.")

            cambios = {}

            nuevo_motivo = simpledialog.askstring("Actualizar Sanción", f"Motivo actual ({sancion.motivo}):") or ""
            nueva_fecha = simpledialog.askstring("Actualizar Sanción", f"Fecha actual ({sancion.fecha_sancion}) [YYYY-MM-DD]:") or ""
            nuevo_monto = simpledialog.askstring("Actualizar Sanción", f"Monto actual ({sancion.monto}):") or ""

            if messagebox.askyesno("Actualizar Sanción", "¿Desea cambiar el cliente de esta sanción?"):
                nuevo_cliente = self.seleccionar_cliente(id_biblioteca)
                if nuevo_cliente:
                    cambios["cod_cliente"] = nuevo_cliente.codigo

            if nuevo_motivo.strip():
                cambios["motivo"] = nuevo_motivo.strip()

            if nueva_fecha.strip():
                try:
                    cambios["fecha_sancion"] = date.fromisoformat(nueva_fecha.strip())
                except ValueError:
                    messagebox.showerror("Error", "Formato de fecha inválido. Use YYYY-MM-DD.")
                    return

            if nuevo_monto.strip():
                try:
                    cambios["monto"] = float(nuevo_monto.strip())
                except ValueError:
                    messagebox.showerror("Error", "Monto inválido. Debe ser un número.")
                    return

            if cambios:
                sancion_actualizada = self.sancion_crud.actualizar_sancion(sancion.id_sancion, id_biblioteca=id_biblioteca, **cambios)

                cliente = cast(Cliente, sancion_actualizada.cliente)

                mensaje = (
                    "Sanción actualizada exitosamente:\n\n"
                    f"ID: {sancion_actualizada.id_sancion}\n"
                    f"Motivo: {sancion_actualizada.motivo}\n"
                    f"Fecha: {sancion_actualizada.fecha_sancion}\n"
                    f"Monto: {sancion_actualizada.monto}\n"
                    f"Cliente: {cliente.nombre}\n"
                )
                messagebox.showinfo("Éxito", mensaje)
            else:
                messagebox.showinfo("Sin cambios", "No se realizaron modificaciones.")

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Error: {e}")

    def eliminar_sancion(self, id_biblioteca: UUID) -> None:
        """Elimina una sanción de la base de datos.
        Solicita confirmación antes de proceder.
        Returns None"""

        try:
            sancion = self.seleccionar_sancion(id_biblioteca)
            if not sancion:
                return

            sancion = self.sancion_crud.obtener_sancion(sancion.id_sancion, id_biblioteca)

            if not sancion:
                messagebox.showerror("Error", "Sanción no encontrada.")
                return

            cliente = cast(Cliente, sancion.cliente)
            confirmacion = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro de eliminar la sanción ID {sancion.id_sancion}?\n"
                f"Motivo: {sancion.motivo}\nCliente: {cliente.nombre}"
            )

            if confirmacion:
                if self.sancion_crud.eliminar_sancion(sancion.id_sancion, id_biblioteca=id_biblioteca):
                    mensaje = (f"La sanción ID {sancion.id_sancion} fue eliminada exitosamente.\n")

                    sanciones_restantes = self.sancion_crud.obtener_sanciones_por_cliente(sancion.cod_cliente, id_biblioteca=id_biblioteca)
                    cliente = self.cliente_crud.obtener_cliente(sancion.cod_cliente, id_biblioteca=id_biblioteca)

                    if not sanciones_restantes and cliente:  
                        self.cliente_crud.actualizar_vetado(sancion.cod_cliente, id_biblioteca=id_biblioteca, vetado=False)
                        mensaje += (f"El cliente '{cliente.nombre}' (Código {cliente.codigo}) ya no se encuentra vetado.")

                    messagebox.showinfo("Éxito", mensaje)
                else:
                    messagebox.showerror("Error", "No se pudo eliminar la sanción.")
            else:
                messagebox.showinfo("Cancelado", "Operación cancelada.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")



    def ejecutar(self) -> None:
        """Ejecutar el sistema principal con autenticación usando diálogos"""
        try:
            create_tables()
            messagebox.showinfo("Sistema", "Sistema listo para usar.")

            if not self.mostrar_pantalla_login():
                messagebox.showwarning("Acceso Denegado", "Usuario o contraseña incorrecta")
                return

            self.mostrar_menu_principal_autenticado()

        except KeyboardInterrupt:
            messagebox.showinfo("Interrupción", "Sistema interrumpido por el usuario.")
        except Exception as e:
            messagebox.showerror("Error crítico", f"{e}")
        finally:
            self.db.close()

def main():
    """Funcion principal"""
    with SistemaGestion() as sistema:
        sistema.ejecutar()

if __name__ == "__main__":
    main()