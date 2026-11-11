from fastapi import FastAPI
from routers import users_router

app = FastAPI()
app.include_router(users_router.router)

@app.get("/")
def read_root():
    mensaje = "Primer TP de FastAPI"
    return  {"message":mensaje}

