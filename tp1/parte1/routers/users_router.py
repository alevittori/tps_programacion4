from typing import Optional

from fastapi import APIRouter, HTTPException, status
from models.users import (
    User,
    GetUsersResponse,
    CreateUserResponse,
    DeleteUserResponse,
    UpDateUserResponse,
)

router = APIRouter()

usuarios: list[User] = [
    User(id=1, name="juan perez"),
    User(id=2, name="pepe sanchez"),
]


#Buscar/listar usuarios filtrando por estado: activos, inactivos, o todos (por ejemplo vía un query param is_active).
@router.get("/user")
def get_users(is_active:Optional[bool]= None) -> GetUsersResponse:
    
    if is_active is None:
        return GetUsersResponse(users=usuarios)
    
    
    usuarios_filtrados = [user for user in usuarios if user.is_active == is_active]
    
    return GetUsersResponse(users=usuarios_filtrados)


#Eliminar un usuario por id (DELETE).
@router.delete("/user/{id}")
def delete_user(id: int) -> DeleteUserResponse:
    for user in usuarios:
        if user.id == id:
            usuarios.remove(user)
            return DeleteUserResponse(message="ususario borrado")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
    )


@router.post("/user")
def create_user(user: User) -> CreateUserResponse:
    usuarios.append(user)
    return CreateUserResponse(message="usuario creado")


#Modificar los datos de un usuario existente (PUT o PATCH).
@router.put("/user/{id}")
def update_user(id: int, user_actualizado: User) -> UpDateUserResponse:
    for user in usuarios:
        if user.id == id:
            user.name = user_actualizado.name
            user.is_active = user_actualizado.is_active
            
            return UpDateUserResponse(message="usuario actualizado")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
    )