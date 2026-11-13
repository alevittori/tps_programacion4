from fastapi import FastAPI
from app.database import create_db_and_tables

# Inicializamos la aplicación FastAPI
app = FastAPI(
    title="Sistema de Biblioteca API",
    version="1.0.0",
    description="API REST para gestionar el catálogo de una biblioteca y sus préstamos (FastAPI + SQLModel)"
)

# Evento que se ejecuta al arrancar la aplicación
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Ruta raíz de prueba para verificar que el servidor responde
@app.get("/")
def read_root():
    return {"mensaje": "¡Bienvenido al Sistema de Biblioteca API! El servidor está funcionando correctamente."}