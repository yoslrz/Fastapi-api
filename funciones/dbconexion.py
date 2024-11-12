import uuid
from funciones.funciones import generar_sql
from funciones.models import models
from funciones.models_object import Acceso
import mysql.connector

    
class MiObjetoMySQL:
    def __init__(self, host: str = '127.0.0.1', user: str = "root", password: str = "12345678"):
        """"Se inicia la instancia para la gestion de la base de datos de MySQL

        Args:
            host (str, optional):  nombre de la base de datos. Defaults to '127.0.0.1'.
            user (str, optional): nombre del usuario para autenticar con el servidor. Defaults to "root".
            password (str, optional): Contraseña para autenticacion en el servidor. Defaults to "".
        """        
        # Establecer la conexión con la base de datos MySQL.
        self.conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
        )
        # Crear el cursor.
        self.cursor = self.conexion.cursor(buffered=True)
        self.cursor.execute('CREATE DATABASE IF NOT EXISTS db_maestra')
        self.cursor.execute('USE db_maestra')
        for i in models:
            self.cursor.execute(i)
            self.conexion.commit()
        print(self.esta_vacio("accesos"))
    
        if self.esta_vacio("accesos"):
            info_acceso = Acceso(**{"id":str(uuid.uuid4()),"correo":"correo@gmail.com","password":"pass123","rol":"Admin"})
            print(self.ingreso_registro("accesos",dict(info_acceso)))


    def esta_vacio(self,nom_tabla:str)->bool:
        """valida si la tabla esta vacia

        Args:
            nom_tabla (str): nombre de la tabla

        Returns:
            bool: False cuando no esta vacia y True cuando si lo esta
        """        
        sql = f"SELECT LAST_INSERT_ID() FROM {nom_tabla}"
        self.cursor.execute(sql)
        x =self.cursor.fetchone()
        if type(x)  == tuple:
            return False
        return True
            
    def ingreso_registro(self,tabla:str,registro:dict):
        """Funcion para ingresar un registro dentro de la db

        Args:
            tabla (str): nombre de la tabla
            registro (dict): modelo a ingresar

        Returns:
            bool|Exception: True en caso de exito, Excepcion en caso de error
        """
        self.cursor.execute("BEGIN")
        sql = generar_sql(tabla,registro)
        # print(sql)
        try:
            self.cursor.execute(sql)
            self.conexion.commit()
            return True
        except Exception as e:
            print(e,"*********")
            return Exception()

    def actualiza_registro(self,tabla:str,datos:list,condicion:str|bool= False)->bool| Exception:
        """Funcion para actualizar los registros de la db

        Args:
            tabla (str): nombre de la tabla
            datos (list): lista de datos a actualizar
            condicion (str | bool, optional): condicion para realizar la actualizacion. Defaults to False.

        Returns:
            bool| Exception: True en caso de exito, Excepcion en otro caso 
        """
        if not condicion:
            sql = f"UPDATE {tabla} SET {','.join(datos)}"
        else:
            sql = f"UPDATE {tabla} SET {','.join(datos)} WHERE {condicion}"
        # print(sql , "--------------------> SQL")
        self.cursor.execute("BEGIN")
        try:
            self.cursor.execute(sql)
            self.cursor.commit()
            return True
        except Exception as e:
            print(e)
            return Exception()
        
    def busca(self,tabla:str,campos:str,condicion:str|bool = False,aux_c:str|bool =False):
        """Funcion para buscar datos dentro de la db

        Args:
            tabla (str): nombre de la tabla
            campos (str): nombre de los campos buscar
            condicion (str | bool, optional): condicion del sql. Defaults to False.

        Returns:
            list|Excepcion: lista con los datos encontrados o Excepcion en caso de error
        """ 
        info = []
        self.cursor.execute("BEGIN")
        if not condicion:
            sql = f"SELECT {campos} FROM {tabla} "
        else:
            sql = f"SELECT {campos} FROM {tabla} WHERE {condicion}"
        # print(sql)
        if aux_c:
            sql = sql+aux_c
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            for res in result:
                info.append(dict(zip(self.cursor.column_names,res)))
        except Exception as e:
            print(e)
            return Exception()
        return info
   

















sql_instance = MiObjetoMySQL()