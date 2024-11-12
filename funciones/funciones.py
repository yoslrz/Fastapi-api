import re
import datetime
import hashlib
import json
from fastapi import Depends
from jose import jwt

SECRETKEY = 'PRUEBATECNICA'
ALGORITH = 'HS256'

def generar_sql(tabla:str,modelo:object)->str: 
    """Funcion para generar el sql

    Args:
        tabla (str): nombre de la tabla
        modelo (object): modelo del que se quiere crear el sql

    Returns:
        str: consulta sql insert
    """ 
    valores_str =[]
    valores = list(dict(modelo).values())
    campos = list(dict(modelo))
    for i in valores:
        if isinstance(i, dict) or isinstance(i, list): 
            i = f"{json.dumps(i)}"
        i= f"'{str(i)}'" 
        valores_str.append(i)
    texto_valores = f'({",".join(valores_str)})'
    texto_campos = f'({",".join(campos)})'
    sql = f"INSERT INTO {tabla} {texto_campos} VALUES {texto_valores}"
    return sql 

def generar_hash_sha256(contrasena)->str:
    """Genera un hash de una cadena

    Args:
        contrasena (_type_): cadena a la que se le genera el hash

    Returns:
        str: hash
    """    
    contrasena_bytes = contrasena.encode('utf-8')
    sha256_hash = hashlib.sha256()
    sha256_hash.update(contrasena_bytes)
    hash_hexadecimal = sha256_hash.hexdigest()
    return hash_hexadecimal

def crear_acces_token(info_user: dict, days: int = 3)-> str:
    """Esta funcion crea un token de acceso para el usuario.

    Args:
        info_user (dict): informacion del usuario al que se le creara el token 
        days (int, optional): número de días . Defaults to 3.

    Returns:
       str: token
    """    
    to_encode = info_user.copy()
    expire = datetime.utcnow() + datetime.timedelta(days=days)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRETKEY, algorithm=ALGORITH)
    return encoded_jwt

'''async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
        status_code=404,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"})
    try:
        info = jwt.decode(token, SECRETKEY, algorithms=[ALGORITH])
        username = info.get("user")
        fecha_ven = datetime.datetime.fromtimestamp(info.get("exp"))
        vigencia = fecha_ven - datetime.datetime.utcnow()
        if username is None and vigencia.total_seconds() <= 0:
            raise exception
    except:
        raise exception
    usuario = sql_instance.usuario_info_by_correo(username)
    try:
        if usuario.estatus == 0:
            raise exception
    except:
        raise HTTPException(status_code=404, detail="Tu usuario ha sido desactivado por token incorrecto contacta a soporte@inein.mx")
    permisos_extra = mongo_instances.obtener_permisos(usuario.id)
    permisos_regulares={}
    if len(permisos_extra) == 0 and usuario.id.split("-")[0] == "socio":
        raise HTTPException(status_code=404, detail="Tu usuario ha sido desactivado contacta a soporte@inein.mx")
    dias_descanso = False
    if usuario.id.split("-")[0] == "colaborador":
        info_col = sql_instance.obtener_colaborador_by_id(usuario.id)
        empresa = sql_instance.empresa_by_id(info_col.empresa)
        info_entidad = sql_instance.obtener_entidad("colaborador","id",usuario.id)
        dias_descanso=info_col.dias_descanso
        try:
            lapicito = lapicito_super_editor(empresa.id_empresa)
        except:
            raise HTTPException(status_code=404, detail="Error al obtener conexion con la base de datos contacta a soporte@inein.mx")
        info_rol = lapicito.obtener_info_rol_by_id(info_col.id_rol)
        del lapicito
        manguito =MyMoanguitoConexion(empresa.id_empresa)
        permisos_regulares = manguito.obtener_permisos(info_rol.id)
        if not permisos_regulares:
            raise HTTPException(status_code=404, detail="Tu usuario ha sido desactivado contacta a soporte@inein.mx")
        actualiza = vacaciones_reset(usuario.id,empresa.id_empresa,info_entidad[0]["fecha_ingreso"])
        if type(actualiza) == Exception:
            raise HTTPException(status_code=404, detail=f"Error {actualiza}")
    permisos_unidos=juntar_permisos({"permisos_extra":permisos_extra,"permisos_regulares":permisos_regulares})
    if not permisos_unidos:
        raise HTTPException(status_code=404, detail="Tu usuario ha sido desactivado contacta a soporte@inein.mx")
    permisos_traducidos = {}
    for key, value in permisos_unidos.items():
        if key == "Usuario_Maestro":
            nombre_empresa = key
        else:
            empresa = sql_instance.empresa_by_id(key)
            if not empresa:
                continue
            if empresa.estatus != 1:
                continue
            nombre_empresa = empresa.nombre
        permisos_traducidos[nombre_empresa] = value
    autorizaciones = sql_instance.busca_autorizaciones({"id_autorizador":usuario.id,"estatus":0})
    if type(autorizaciones) == Exception:
      autorizaciones = []
    return {"access_token": token, "token_type": "bearer", 'session': {'id': usuario.id, 'email': usuario.correo, 'tema': usuario.tema, "animacion": usuario.animacion, "nombre": usuario.nombre, "apellido1": usuario.apellido_paterno, "apellido2": usuario.apellido_materno,"img_perfil":usuario.img_perfil,"api":usuario.api,"dias_descanso":dias_descanso}, "permisos": permisos_traducidos,"autorizaciones_pendientes":autorizaciones}
'''
def valida_curp(cadena:str):
    patron = r"^[A-Z]{4}\d{6}[HM]{1}[A-Z]{2}[B-DF-HJ-NP-TV-Z]{3}[A-Z\d]{1}\d{1}$"
    return bool(re.match(patron, cadena))

def valida_rfc(cadena:str):
    patron = r"^[A-ZÑ&]{3,4}\d{6}[A-Z\d]{3}$"
    return bool(re.match(patron,cadena))