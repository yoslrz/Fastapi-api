from pydantic import BaseModel
from typing import List

class Acceso(BaseModel):
    id:str | bool = False
    correo: str
    password: str|bool = False
    rol:str

class Usuarios(BaseModel):
    correo:str
    password:str
    rol:str
    nombre:str
    apellido_paterno:str
    apellido_materno:str|bool=False
    curp:str
    rfc:str
    calle:str
    colonia:str
    codigo_postal:str
    delegacion:str
