from typing import Annotated, Sequence
from fastapi import Depends
from sqlmodel import select, func
from app.database import SessionDep
from app.models.prestamo import Prestamo

class PrestamoRepository:
    def __init__(self, session: SessionDep):
        self.session = session

    def create(self, prestamo: Prestamo) -> Prestamo:
        self.session.add(prestamo)
        self.session.commit()
        self.session.refresh(prestamo)
        return prestamo

    def get_all(self, skip: int = 0, limit: int = 100, activos: bool | None = None) -> Sequence[Prestamo]:
        statement = select(Prestamo)
        
        if activos is True:
            statement = statement.where(Prestamo.fecha_devolucion == None)
        elif activos is False:
            statement = statement.where(Prestamo.fecha_devolucion != None)
            
        statement = statement.offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def get_by_id(self, prestamo_id: int) -> Prestamo | None:
        return self.session.get(Prestamo, prestamo_id)

    def get_by_socio(self, socio_id: int, activos: bool | None = None) -> Sequence[Prestamo]:
        statement = select(Prestamo).where(Prestamo.socio_id == socio_id)
        
        if activos is True:
            statement = statement.where(Prestamo.fecha_devolucion == None)
        elif activos is False:
            statement = statement.where(Prestamo.fecha_devolucion != None)
            
        return self.session.exec(statement).all()

    def count_activos_by_socio(self, socio_id: int) -> int:
        statement = select(func.count()).select_from(Prestamo).where(
            Prestamo.socio_id == socio_id,
            Prestamo.fecha_devolucion.is_(None)
        )
        return self.session.exec(statement).one()

    def update(self, prestamo_db: Prestamo) -> Prestamo:
        self.session.add(prestamo_db)
        self.session.commit()
        self.session.refresh(prestamo_db)
        return prestamo_db
    
    

PrestamoRepositoryDep = Annotated[PrestamoRepository, Depends(PrestamoRepository)]