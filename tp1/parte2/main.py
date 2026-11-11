from fastapi import FastAPI
from routers import routers_cafe 
app = FastAPI()
app.include_router(routers_cafe.router)


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a Cafe Vitt"}