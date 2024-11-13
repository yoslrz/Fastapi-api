### Prueba tecnica Ariadne Lara
# Descripcion:
    API para la administracion de usuarios con diferentes controles de acesso 
# Lenguaje 
    python 3.10.7 
# Framework
    Fast API
# Base de datos 
    mysql,cambiar nombre de usuario asi como contrasenia donde se ejecute
# Instrucciones de uso
    1. Colonar el repositrorio 
    2. Crear un entorno virtual 
        comando en windows: python -m venv venv, donde el segundo venv es el nombre del entorno virtual
    3. Activar entorno virtual
        comando: 
    4. Instalar librerias y framework con el comando
        pip install -r requirements.txt
    5. Cuando se acabe de instalar ejecutaremos el comando 
        python -m uvicorn main:app --reload --port 4000 --host 192.168.0.115
# Datos importantes
    se creo por defecto un acceso con el rol de Admin, para poder crear mas apartir de el, el ingreso debe hacerse con el correo: correo@gmail.com y la contrasenia: pass123
    El cuerpo solicitado para un nuevo usuario es el siguiente:
        {correo:str,password:str,rol:str,nombre:str,apellido_paterno:str,apellido_materno:str|bool=False,curp:str,rfc:str,calle:str,colonia:str,codigo_postal:str,delegacion:str}
    de acuerdo al modelo Usuarios en models_object
    De igual manera el tipo esperado para editar usuarios es:
        {nombre:str,apellido_paterno:str,apellido_materno:str|bool=False,curp:str,rfc:str}
    y para editar su informacion de usuario es:
        {calle:str,colonia:str,codigo_postal:str,delegacion:str}