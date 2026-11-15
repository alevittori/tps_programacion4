from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import autor_router,libro_router


# Inicializamos la aplicación FastAPI
app = FastAPI()

app.include_router(autor_router.router)
app.include_router(libro_router.router)
# Evento que se ejecuta al arrancar la aplicación
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Ruta raíz de prueba para verificar que el servidor responde
@app.get("/")
def read_root():
    return {"mensaje": "¡Bienvenido al Sistema de Biblioteca API! El servidor está funcionando correctamente."}