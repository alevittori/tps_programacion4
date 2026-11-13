from datetime import date
from sqlmodel import Relationship, SQLModel, Field

from tp2.app.models.libro import Libro
from tp2.app.models.socio import Socio

# 1. Atributos base compartidos
class PrestamoBase(SQLModel):
    fecha_prestamo: date
    fecha_vencimiento: date
    fecha_devolucion: date | None = None  # Nulo hasta que se devuelva el libro
    multa: float = Field(default=0.0)      # Arranca en 0

# 2. Modelo para CREAR un préstamo (POST /prestamos)
# Generalmente el cliente manda a qué socio y qué libro le presta; las fechas 
# y la multa las suele calcular el servicio automáticamente por regla de negocio.
class PrestamoCreate(SQLModel):
    socio_id: int = Field(foreign_key="socios.id")
    libro_id: int = Field(foreign_key="libros.id")

# 3. Modelo para ACTUALIZAR un préstamo (por si hace falta modificar algo)
class PrestamoUpdate(SQLModel):
    fecha_devolucion: date | None = None
    multa: float | None = None

# 4. Modelo de BASE DE DATOS (Tabla real)
class Prestamo(PrestamoBase, table=True):
    __tablename__ = "prestamos"
    
    id: int | None = Field(default=None, primary_key=True)
    
    # Claves foráneas que apuntan a las otras tablas
    socio_id: int = Field(foreign_key="socios.id")
    libro_id: int = Field(foreign_key="libros.id")
    
    # Relaciones inversas N-1
    socio: Socio = Relationship(back_populates="prestamos")
    libro: Libro = Relationship(back_populates="prestamos")