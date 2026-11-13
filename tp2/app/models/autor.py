
from sqlmodel import Relationship, SQLModel, Field

from tp2.app.models.libro import Libro
from tp2.app.models.libro_autor import LibroAutorLink

class AutorBase(SQLModel):
    nombre:str 
    nacionalidad: str 
    
    
class AutorCreate(AutorBase):
    pass  


class AutorUpdate(SQLModel):
    nombre: str | None = None
    nacionalidad: str | None = None

class Autor(AutorBase, table = True):
    __tablename__ = "autores"
    id: int | None = Field(default=None, primary_key=True)
    
    # Relación N-N con Libros usando la tabla intermedia
    libros: list[Libro] = Relationship(back_populates="autores", link_model=LibroAutorLink)