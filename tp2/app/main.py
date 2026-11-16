from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import autor_router,libro_router,socio_router


# Inicializamos la aplicación FastAPI
app = FastAPI()

app.include_router(autor_router.router)
app.include_router(libro_router.router)
app.include_router(socio_router.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def read_root():
    return {"mensaje": "¡Bienvenido al Sistema de Biblioteca."}