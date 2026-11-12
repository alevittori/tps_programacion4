
from sqlmodel import SQLModel, Field

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
    