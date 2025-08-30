# 📚 Sistema de Gestión de Biblioteca

Este proyecto implementa un sistema de gestión de biblioteca con **Python** tilizando principios de **Programación Orientada a Objetos (POO)** como **herencia, polimorfismo, encapsulamiento y reutilización de código** y **Tkinter** para la interacción mediante ventanas emergentes.  

Permite administrar **clientes**, **material bibliográfico** y **préstamos**, incluyendo funcionalidades de búsqueda, reserva, renovación y devoluciones.  

## 🗂️ Estructura del proyecto
- `main.py` → Archivo principal que contiene los menús e inicia la aplicación.  
- `Biblioteca.py` → Lógica central del sistema (gestión de clientes, materiales, préstamos y reservas).  
- `Cliente.py` → Definición de las clases `Cliente`, `Estudiante`, `Profesor` y `Empleado`.  
- `Material_Bibliografico.py` → Manejo de los materiales (estado, reservas, disponibilidad).  
- `Prestamo.py` → Definición de la clase `Prestamo` y sus operaciones.  

## ⚙️ Requisitos
Antes de ejecutar el proyecto, asegúrate de tener instalado:  
- Python **3.9+**  
- Tkinter (viene incluido en la mayoría de instalaciones de Python)  

## ▶️ Ejecución paso a paso
1. **Clonar o descargar el repositorio en *Visual Studio Code***  
   ```bash
   git clone <URL-del-repositorio>
   ```

2. **Verificar que todos los archivos están en la misma carpeta**:  
   - `main.py`  
   - `Biblioteca.py`  
   - `Cliente.py`  
   - `Material_Bibliografico.py`  
   - `Prestamo.py`

3. **Ejecutar el archivo principal**  
   ```bash
   python main.py
   ```

4. **Uso del programa**  
   - Al ejecutar, se abrirá el **menú principal** con opciones:  
     1. Gestión de clientes  
     2. Gestión de materiales bibliográficos  
     3. Gestión de préstamos  
     0. Salir  
     
   - Dentro de cada sección podrás:  
     - **Clientes**: agregar, buscar, ver listado y ver clientes vetados.  
     - **Materiales**: agregar, buscar, ver listado, reservar y cancelar reservas.  
     - **Préstamos**: prestar material, ver préstamos, buscar, renovar, devolver y eliminar préstamos.  

5. **Interfaz gráfica**  
   Todas las interacciones se hacen mediante **ventanas emergentes (messagebox y simpledialog de Tkinter)**.  

## 👨‍💻 Autores
Proyecto académico desarrollado en Python por: ***Maria Fernanda Palacio*** y ***Salomé Gil***
***2025***

