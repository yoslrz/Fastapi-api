from datetime import datetime
import uuid
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from funciones.dbconexion import sql_instance
from funciones.funciones import ALGORITH, crear_acces_token, generar_hash_sha256,SECRETKEY, valida_curp, valida_rfc
from funciones.models_object import Acceso, Usuarios,UsuarioEdit,Domicilio
from jose import jwt

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl='/')

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    usuario = sql_instance.busca("accesos","*",f"correo = '{form.username}'")
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


@router.get("/validador")
async def validador_tok(token:str=Depends(oauth2)): 
    exception = HTTPException(
        status_code=404,
        detail= {"texto":"Credenciales de autenticación inválidas"} ,
        headers={"WWW-Authenticate": "Bearer"})
    try:
        info = jwt.decode(token, SECRETKEY, algorithms=[ALGORITH])
        fecha_ven = datetime.fromtimestamp(info.get("exp"))
        id_user = info.get('id')
        vigencia = fecha_ven - datetime.now()
        if vigencia.total_seconds() <= 0:
            raise exception
    except Exception as e:
        raise exception
    info_us = sql_instance.busca(tabla="accesos",condicion=f"id ='{id_user}'",campos="*")
    if type(info_us) == Exception:
        raise HTTPException(status_code=500,detail="Error al obtener info de la base de datos")
    if len(info_us) == 0:
        raise HTTPException(status_code=406,detail="Usuario no encontrado")
    info_us = info_us[0]
    return {"correo": info_us["correo"], "id": info_us["id"]} 

@router.post("/usuarios")
async def nuevo_usuario(info_usuario:Usuarios,user:str=Depends(validador_tok)):
    rol = sql_instance.busca("accesos","rol",f"id = {user['id']}")
    if type(rol) == Exception:
        raise HTTPException(status_code=406,detail="Error en la consulta de la base de datos")
    if len(rol)<1:
        raise HTTPException(status_code=406,detail="Usuario no encontrado")
    if rol[0]['rol'] not in ["Admin"]:
        raise HTTPException(status_code=403,detail="Usuario sin permisos")
    if info_usuario.rol not in ["Admin","Edicion","Consulta"]:
        raise HTTPException(status_code=406,detail="Los roles validos solo son admin,edicion y consulta")
    if not valida_curp(info_usuario.curp):
        raise HTTPException(status_code=406,detail="Formato de curp invalido")
    if not valida_rfc(info_usuario.rfc):
        raise HTTPException(status_code=406,detail="Formato de rfc invalido")
    if type(info_usuario.codigo_postal) != int or len(info_usuario.codigo_postal) < 5 or len(info_usuario.codigo_postal) > 5:
        raise HTTPException(status_code=406,detail="Formato de codigo postal invalido")
    accesso = {"id":uuid.uuid4(),"correo":info_usuario.correo,"password":info_usuario.password,"rol":info_usuario.rol}
    usuarios = {"id":uuid.uuid4(),'curp':info_usuario.curp,'rfc':info_usuario.rfc,'nombre':info_usuario.nombre,'apellido_paterno':info_usuario.apellido_paterno,'apellido_materno':info_usuario.apellido_materno,'id_acceso':accesso['id']}
    domicilio = {"id":uuid.uuid4(),'calle':info_usuario.calle,'colonia':info_usuario.colonia,'codigo_postal':info_usuario.codigo_postal,'delegacion':info_usuario.delegacion,'id_usuario':usuarios['id']}
    accesos_r = sql_instance.ingreso_registro("accesos",accesso)
    usuarios_r = sql_instance.ingreso_registro("usuarios",usuarios)
    info_r = sql_instance.ingreso_registro("info_domicilio",domicilio)
    if type(accesos_r) == Exception or type(usuarios_r) or type(info_r):
        raise HTTPException(status_code=406,detail="Error en la consulta de la base de datos")
    return {'message':'usaurio registrado'}

@router.get("/consulta")
async def consulta(user:str=Depends(validador_tok)):
    rol = sql_instance.busca(tabla="accesos",campos="rol",condicion=f"id = '{user['id']}'")
    if type(rol) == Exception:
        raise HTTPException(status_code=406,detail="Error en la consulta de la base de datos")
    if len(rol)<1:
        raise HTTPException(status_code=406,detail="Usuario no encontrado")
    rol_user = rol[0]['rol']
    dicc_consulta = {"Admin":"usuarios","Consulta":"usuarios","Edicion":"info_domicilio"}
    if rol_user not in dicc_consulta:
        raise HTTPException(status_code=403,detail="Usuario sin permisos") 
    consulta = sql_instance.busca(tabla=dicc_consulta[rol_user],campos="*",condicion="fecha_eliminacion IS NULL")
    if type(consulta) == Exception:
        raise HTTPException(status_code=406,detail="Error en la consulta de la base de datos")
    return consulta

@router.put("/actualizar/{id}")
async def actualiza(info:dict,id:str,user:str=Depends(validador_tok)):
    rol = sql_instance.busca(tabla="accesos",campos="rol",condicion=f"id = '{user['id']}'")
    if type(rol) == Exception:
        raise HTTPException(status_code=406,detail="Error en la consulta de la base de datos")
    if len(rol)<1:
        raise HTTPException(status_code=406,detail="Usuario no encontrado")
    rol_user = rol[0]['rol']
    dicc_consulta = {"Admin":{"tabla":"usuarios","modelo":UsuarioEdit},"Edicion":{"tabla":"info_domicilio","modelo":Domicilio}}
    if rol_user not in dicc_consulta:
        raise HTTPException(status_code=403,detail="Usuario sin permisos")
    modelo = dicc_consulta[rol_user]['modelo']
    tabla = dicc_consulta[rol_user]['tabla']
    verifica_info = sql_instance(tabla,"*",f"id = '{id}'")
    if type(verifica_info) == Exception:
        raise HTTPException(status_code=406,detail="Error en la consulta de la base de datos")
    if len(verifica_info)<1:
        raise HTTPException(status_code=406,detail="Informacion no encontrado")
    try:
        info_verificada = modelo(**info)
    except:
       raise HTTPException(status_code=403,detail="Informacion erronea") 
    informacion = dict(info_verificada)
    condiciones = []
    for key,value in informacion.items():
        condiciones.append(f"{key} = '{value}'")
    actualiza = sql_instance.actualiza_registro(tabla,condiciones,condicion=f"id = '{id}'")
    if type(actualiza) == Exception:
        raise HTTPException(status_code=406,detail="Error en la consulta de la base de datos")
    return {'message':'Informacion Actualizada con exito'}

@router.delete("/eliminar/{id}")
async def nuevo_usuario(id:str,user:str=Depends(validador_tok)):
    rol = sql_instance.busca("accesos","rol",f"id = {user['id']}")
    if type(rol) == Exception:
        raise HTTPException(status_code=406,detail="Error en la consulta de la base de datos")
    if len(rol)<1:
        raise HTTPException(status_code=406,detail="Usuario no encontrado")
    if rol[0]['rol'] not in ["Admin"]:
        raise HTTPException(status_code=403,detail="Usuario sin permisos")
    verifica_info = sql_instance("usuarios","*",f"id = '{id}'")
    if type(verifica_info) == Exception:
        raise HTTPException(status_code=406,detail="Error en la consulta de la base de datos")
    elimina = sql_instance.elimina_registro("usuarios",f"id = '{id}'")
    if type(elimina) == Exception:
        raise HTTPException(status_code=406,detail="Error en la consulta de la base de datos")
    return {"message":"Informacion eliminada con exito"}