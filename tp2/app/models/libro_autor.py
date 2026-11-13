from sqlmodel import SQLModel, Field

# tabla intermedia para la relacion Libro N-N Autor
class LibroAutorLink(SQLModel, table=True):
    __tablename__ = "libro_autor"
    
    libro_id: int | None = Field(default=None, foreign_key="libros.id", primary_key=True)
    autor_id: int | None = Field(default=None, foreign_key="autores.id", primary_key=True)