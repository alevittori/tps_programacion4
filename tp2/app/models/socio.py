from sqlmodel import Relationship, SQLModel, Field

#from app.models.prestamo import Prestamo

# 1. Atributos base compartidos
class SocioBase(SQLModel):
    nombre: str
    email: str = Field(unique=True, index=True)  # Único y con índice para validar duplicados y buscar rápido
    activo: bool = Field(default=True)           # Por defecto un socio nuevo nace activo

# 2. Modelo para CREAR un socio (POST)
class SocioCreate(SocioBase):
    pass  # Hereda nombre, email y activo (si no lo mandan, toma el default True)

# 3. Modelo para ACTUALIZAR un socio (PUT/PATCH) - Todos los campos opcionales
class SocioUpdate(SQLModel):
    nombre: str | None = None
    email: str | None = None
    activo: bool | None = None

# 4. Modelo de BASE DE DATOS (Tabla real)
class Socio(SocioBase, table=True):
    __tablename__ = "socios"
    
    id: int | None = Field(default=None, primary_key=True)
    
    # Relación 1-N con Préstamos (Un socio puede tener varios préstamos)
    prestamos: list["Prestamo"] = Relationship(back_populates="socio")