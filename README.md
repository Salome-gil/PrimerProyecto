# Sistema de Gestión de Biblioteca  

Este proyecto implementa un sistema de gestión de biblioteca con *Python, utilizando principios de **Programación Orientada a Objetos (POO)* como *herencia, polimorfismo, encapsulamiento y reutilización de código, además de **Tkinter* para la interfaz gráfica mediante ventanas emergentes.  

Ahora, el sistema se integra con una *base de datos en la nube (Neon)* usando *SQLAlchemy ORM*, lo que permite un manejo más robusto y escalable de la información.  

El sistema administra *clientes, **material bibliográfico, **sedes, **usuarios, **reservas, **sanciones* y *categorías*, incluyendo funcionalidades de búsqueda, registro, préstamos, renovaciones y devoluciones.  

---

## Estructura del proyecto
- main.py → Archivo principal que contiene los menús e inicia la aplicación.  
- Biblioteca.py → Lógica central del sistema (gestión de clientes, materiales, préstamos, reservas y base de datos).  
- Cliente.py → Definición de las clases Cliente, Estudiante, Profesor y Empleado.  
- Material_Bibliografico.py → Manejo de materiales (estado, reservas, disponibilidad).  
- Prestamo.py → Definición de la clase Prestamo y sus operaciones.  
- Sede.py → Entidad que representa las sedes de la biblioteca.  
- Usuario.py → Entidad que gestiona los usuarios del sistema.  
- Sancion.py → Entidad que administra las sanciones aplicadas a los clientes.  
- Reserva.py → Entidad encargada de las reservas de materiales.  
- Categoria.py → Entidad que clasifica los materiales bibliográficos.  

---

## Requisitos
Antes de ejecutar el proyecto, asegúrate de tener instalado:  
- Python *3.9+*  
- Tkinter (incluido en la mayoría de instalaciones de Python)  
- SQLAlchemy  
- Psycopg2 (para la conexión con PostgreSQL en Neon)  
- Una cuenta y base de datos creada en [*Neon*](https://neon.tech/)  

Instalación de dependencias:  
bash
pip install sqlalchemy psycopg2


---

##  Ejecución paso a paso

1. *Clonar o descargar el repositorio en Visual Studio Code*  
   bash
   git clone <URL-del-repositorio>
   cd <nombre-del-proyecto>
   

2. *Configurar las variables de entorno*  
   Crea un archivo .env en la raíz del proyecto con tu cadena de conexión de Neon:  
   
   DATABASE_URL=postgresql+psycopg2://usuario:password@host/dbname
   

3. *Verificar que todos los archivos están en la carpeta del proyecto*:  
   - main.py  
   - Biblioteca.py  
   - Cliente.py  
   - Material_Bibliografico.py  
   - Prestamo.py  
   - Sede.py  
   - Usuario.py  
   - Sancion.py  
   - Reserva.py  
   - Categoria.py  

4. *Ejecutar el archivo principal*  
   bash
   python main.py
   

5. *Uso del programa*  
   - Al ejecutar, se abrirá el *menú principal* con opciones:  
     1. Gestión de clientes  
     2. Gestión de materiales bibliográficos  
     3. Gestión de préstamos  
     4. Gestión de reservas  
     5. Gestión de sanciones  
     6. Gestión de sedes y categorías  
     0. Salir  

   - Dentro de cada sección podrás:  
     - *Clientes*: agregar, buscar, listar y ver vetados.  
     - *Materiales*: agregar, buscar, listar, reservar, cancelar reservas.  
     - *Préstamos*: prestar material, ver préstamos, buscar, renovar, devolver, eliminar.  
     - *Reservas*: registrar, consultar y cancelar.  
     - *Sanciones*: asignar, consultar y gestionar restricciones.  
     - *Sedes y categorías*: organizar la biblioteca en diferentes sucursales y clasificaciones.  

5.1. **Acceso como administrador**  
   Para probar todas las funcionalidades, puedes usar las siguientes credenciales:

   - Usuario: admin
   - Contraseña: Admin1234!

6. *Interfaz gráfica*  
   Todas las interacciones se realizan mediante *ventanas emergentes (messagebox y simpledialog de Tkinter)*.  

---

##  Autores
Proyecto académico desarrollado en Python con integración ORM y Neon por:  
- **María Fernanda Palacio**  
- **Salomé Gil**  
*2025*