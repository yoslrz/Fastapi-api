*** Prueba tecnica Ariadne Lara
Descripcion:
    API para la administracion de usuarios con diferentes controles de acesso 
Lenguaje 
    python 3.10.7 
Framework
    Fast API
base de datos 
    mysql 
Instrucciones de uso
    1. Colonar el repositrorio 
    2. Crear un entorno virtual 
        comando en windows: python -m venv venv, donde el segundo venv es el nombre del entorno virtual
    3. Activar entorno virtual
        comando: 
    4. Instalar librerias y framework con el comando
        pip install -r requirements.txt
    5. Cuando se acabe de instalar ejecutaremos el comando 
    python -m uvicorn main:app --reload --port 4000 --host 192.168.0.115