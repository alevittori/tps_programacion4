from sqlmodel import SQLModel, create_engine, Session

# Nombre del archivo de base de datos SQLite local
sqlite_file_name = "db_biblioteca.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False es necesario en SQLite para FastAPI por el manejo de hilos concurrentes
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    """Crea las tablas en la base de datos si no existen."""
    # Importamos los modelos acá adentro para asegurarnos de que SQLModel 
    # los reconozca a todos antes de ejecutar el create_all
    from app.models.autor import Autor
    from app.models.libro import Libro
    from app.models.socio import Socio
    from app.models.prestamo import Prestamo
    from app.models.libro_autor import LibroAutorLink

    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependencia de FastAPI que abre una sesión de base de datos por cada request y la cierra al terminar."""
    with Session(engine) as session:
        yield session