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
    expire = datetime.datetime.now() + datetime.timedelta(days=days)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRETKEY, algorithm=ALGORITH)
    return encoded_jwt


def valida_curp(cadena:str):
    patron = r"^[A-Z]{4}\d{6}[HM]{1}[A-Z]{2}[B-DF-HJ-NP-TV-Z]{3}[A-Z\d]{1}\d{1}$"
    return bool(re.match(patron, cadena))

def valida_rfc(cadena:str):
    patron = r"^[A-ZÑ&]{3,4}\d{6}[A-Z\d]{3}$"
    return bool(re.match(patron,cadena))