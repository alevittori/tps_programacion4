from abc import ABC, abstractmethod
from typing import Sequence
from datetime import date, timedelta
from app.models.prestamo import Prestamo, PrestamoCreate, PrestamoUpdate
from app.repositories.prestamo_repository import PrestamoRepositoryDep
from app.repositories.libro_repository import LibroRepositoryDep
from app.repositories.socio_repository import SocioRepositoryDep

MAX_PRESTAMOS_ACTIVOS = 3
DIAS_PLAZO_PRESTAMO = 14
MONTO_MULTA_POR_DIA = 100.0  # Valor exacto de la consigna

class PrestamoServiceInterface(ABC):
    @abstractmethod
    def registrar_prestamo(self, prestamo_in: PrestamoCreate) -> Prestamo:
        ...

    @abstractmethod
    def registrar_devolucion(self, prestamo_id: int) -> Prestamo:
        ...

    @abstractmethod
    def get_prestamos(self, skip: int, limit: int, activos: bool | None) -> Sequence[Prestamo]:
        ...

    @abstractmethod
    def get_prestamo_by_id(self, prestamo_id: int) -> Prestamo | None:
        ...

    @abstractmethod
    def get_prestamos_por_socio(self, socio_id: int, activos: bool | None = None) -> Sequence[Prestamo]:
        ...
    
    @abstractmethod
    def actualizar_prestamo(self, prestamo_id: int, prestamo_in: PrestamoUpdate) -> Prestamo | None:
        ...

class PrestamoService(PrestamoServiceInterface):
    def __init__(
        self,
        repo: PrestamoRepositoryDep,
        libro_repo: LibroRepositoryDep,
        socio_repo: SocioRepositoryDep
    ):
        self.repo = repo
        self.libro_repo = libro_repo
        self.socio_repo = socio_repo

    def registrar_prestamo(self, prestamo_in: PrestamoCreate) -> Prestamo:
        # 1. Validar que el socio exista (404)
        socio = self.socio_repo.get_by_id(prestamo_in.socio_id)
        if not socio:
            raise LookupError("Socio no encontrado.")

        # 2. Validar que el socio esté activo (403)
        if not socio.activo:
            raise PermissionError("El socio se encuentra inactivo y no puede solicitar préstamos.")

        # 3. Validar que el libro exista (404)
        libro = self.libro_repo.get_by_id(prestamo_in.libro_id)
        if not libro:
            raise LookupError("Libro no encontrado.")

        # 4. Validar que haya stock disponible (409)
        if libro.stock <= 0:
            raise ValueError(f"No hay stock disponible para el libro '{libro.titulo}'.")

        # 5. Validar el límite máximo de 3 préstamos activos por socio (409)
        prestamos_activos = self.repo.count_activos_by_socio(socio.id)
        if prestamos_activos >= MAX_PRESTAMOS_ACTIVOS:
            raise ValueError(f"El socio ya alcanzó el límite máximo de {MAX_PRESTAMOS_ACTIVOS} préstamos activos.")

        # 6. Calcular fechas por regla de negocio
        hoy = date.today()
        nuevo_prestamo = Prestamo(
            socio_id=prestamo_in.socio_id,
            libro_id=prestamo_in.libro_id,
            fecha_prestamo=hoy,
            fecha_vencimiento=hoy + timedelta(days=DIAS_PLAZO_PRESTAMO),
            multa=0.0
        )

        # 7. Descontar 1 unidad del stock del libro
        libro.stock -= 1
        self.libro_repo.session.add(libro)

        # 8. Guardar el préstamo
        return self.repo.create(nuevo_prestamo)

    def registrar_devolucion(self, prestamo_id: int) -> Prestamo:
        prestamo = self.repo.get_by_id(prestamo_id)
        if not prestamo:
            raise LookupError("Préstamo no encontrado.")

        if prestamo.fecha_devolucion is not None:
            raise ValueError("Este préstamo ya fue devuelto anteriormente.")

        hoy = date.today()
        prestamo.fecha_devolucion = hoy

        if hoy > prestamo.fecha_vencimiento:
            dias_retraso = (hoy - prestamo.fecha_vencimiento).days
            prestamo.multa = dias_retraso * MONTO_MULTA_POR_DIA

        libro = self.libro_repo.get_by_id(prestamo.libro_id)
        if libro:
            libro.stock += 1
            self.libro_repo.session.add(libro)

        return self.repo.update(prestamo)

    def get_prestamos(self, skip: int = 0, limit: int = 100, activos: bool | None = None) -> Sequence[Prestamo]:
        return self.repo.get_all(skip, limit, activos)

    def get_prestamo_by_id(self, prestamo_id: int) -> Prestamo | None:
        return self.repo.get_by_id(prestamo_id)

    def get_prestamos_por_socio(self, socio_id: int, activos: bool | None = None) -> Sequence[Prestamo]:
        socio = self.socio_repo.get_by_id(socio_id)
        if not socio:
            raise LookupError("Socio no encontrado.")
        return self.repo.get_by_socio(socio_id, activos=activos)
    
    def actualizar_prestamo(self, prestamo_id: int, prestamo_in: PrestamoUpdate) -> Prestamo | None:
        prestamo = self.repo.get_by_id(prestamo_id)
        if not prestamo:
            return None

        if prestamo_in.fecha_devolucion is not None:
            prestamo.fecha_devolucion = prestamo_in.fecha_devolucion
            if prestamo.fecha_devolucion > prestamo.fecha_vencimiento:
                dias_retraso = (prestamo.fecha_devolucion - prestamo.fecha_vencimiento).days
                prestamo.multa = dias_retraso * MONTO_MULTA_POR_DIA
            else:
                prestamo.multa = 0.0

        if prestamo_in.multa is not None:
            prestamo.multa = prestamo_in.multa

        return self.repo.update(prestamo)