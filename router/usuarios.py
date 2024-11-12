from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from funciones.dbconexion import sql_instance
from funciones.funciones import crear_acces_token, generar_hash_sha256
from funciones.models_object import Acceso

router = APIRouter()

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    usuario = sql_instance.busca("accesos","*",f"correo = '{form.username}'","*")
    if type(usuario) == Exception:
        raise HTTPException(status_code=500,detail="Error al obtener informacion de la base de datos")
    if len(usuario) == 0:
        return {"message":"Usuario no registrado"}
    usuario = usuario[0]
    passhash = generar_hash_sha256(form.password)
    if passhash != usuario['password']:
        raise HTTPException(status_code=406,detail="Contrasena invalida")
    token = crear_acces_token(({"user": usuario["correo"], "id": usuario["id"]}))
    return {"token": token}

@router.get("/usuarios")
async def nuevo_usuario():
    pass

@router.post("/usuarios")
async def nuevo_usuario(info_usuario:Acceso):#user=Depends(auth_user)):
    #rol = sql_instance.busca("accesos","rol",f"id = {user}")
    if info_usuario.rol not in ["admin","edicion","consulta"]:
        raise HTTPException(status_code=406,detail="Los roles validos solo son admin,edicion y consulta")
    
    
    

