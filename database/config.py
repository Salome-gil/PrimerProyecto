"""
Configuración de la base de datos PostgreSQL con Neon
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos Neon PostgreSQL
# Obtener la URL completa de conexión desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Si no hay DATABASE_URL, construir desde variables individuales
if not DATABASE_URL:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "neondb")
    DB_USERNAME = os.getenv("DB_USERNAME", "")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    if DB_USERNAME and DB_PASSWORD:
        DATABASE_URL = (
            f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    else:
        raise ValueError(
            "Se requiere DATABASE_URL o las credenciales individuales de la base de datos"
        )

# Crear el motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Mostrar las consultas SQL en consola
    pool_pre_ping=True,  # Verificar conexión antes de usar
    pool_recycle=300,  # Reciclar conexiones cada 5 minutos
)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """
    Generador de sesiones de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Crear todas las tablas definidas en los modelos
    """
    Base.metadata.create_all(bind=engine)