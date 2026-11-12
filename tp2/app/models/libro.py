from sqlmodel import SQLModel, Field

# 1. Atributos base compartidos
class LibroBase(SQLModel):
    titulo: str
    isbn: str = Field(unique=True, index=True)  # Único y con índice para búsquedas rápidas
    stock: int = Field(ge=0)                    # ge=0 asegura que sea mayor o igual a 0 por regla de negocio
    anio: int

# 2. Modelo para CREAR un libro (POST)
class LibroCreate(LibroBase):
    pass  # Hereda todos los campos obligatorios de LibroBase

# 3. Modelo para ACTUALIZAR un libro (PUT/PATCH) - Todos opcionales
class LibroUpdate(SQLModel):
    titulo: str | None = None
    isbn: str | None = None
    stock: int | None = Field(default=None, ge=0)
    anio: int | None = None

# 4. Modelo de BASE DE DATOS (Tabla real)
class Libro(LibroBase, table=True):
    __tablename__ = "libros"
    
    id: int | None = Field(default=None, primary_key=True)