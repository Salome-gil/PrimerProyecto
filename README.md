# Sistema de Gestión de Biblioteca (Versión API)

Este proyecto implementa un **Sistema de Gestión de Biblioteca** desarrollado en **Python**, utilizando principios de **Programación Orientada a Objetos (POO)** y ahora adaptado a un **entorno API**.  
Esta nueva versión permite la comunicación mediante endpoints REST, gestionando la información directamente a través de peticiones HTTP.

## Características principales

- Arquitectura basada en **API REST**.  
- Integración con **ORM (SQLAlchemy)** para manejo de base de datos.  
- Entidades principales: `Sede`, `Usuario`, `Sanción`, `Reserva` y `Categoría`.  
- Conexión con base de datos en la nube mediante **Neon**.  
- Código modular y escalable.  
- Preparado para despliegue y pruebas desde herramientas como **Swagger UI** o **Postman**.  

## Instalación y ejecución

1. **Clona este repositorio:**
   ```bash
   git clone <URL-del-repositorio>
   cd Proyecto
   ```

2. **Instala las dependencias del proyecto:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta la API:**
   ```bash
   uvicorn main:app --reload
   ```

## Estructura del proyecto

```
Proyecto/
│
├── app/
│   ├── models/           # Entidades y relaciones ORM
│   ├── routers/          # Rutas de la API
│   ├── schemas/          # Esquemas Pydantic
│   ├── core/             # Configuración principal
│   └── main.py           # Punto de entrada de la API
│
├── requirements.txt
└── README.md
```

## Notas

- Asegúrate de tener **Python 3.10** o superior.  
- Antes de ejecutar el proyecto, instala los **requirements**.  
- Accede a la documentación interactiva en:  
   `http://127.0.0.1:8000/docs`  

##  Autores
Proyecto académico desarrollado en Python con integración ORM y Neon por:  
- **María Fernanda Palacio**  
- **Salomé Gil**  
*2025*