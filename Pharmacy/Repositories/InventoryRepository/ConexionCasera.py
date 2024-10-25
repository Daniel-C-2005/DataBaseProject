import pyodbc

server='localhost'
bd='Db_ProyectoDB1_1'
usuario='soporte'
contrasenia='123'

try:
    conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; SERVER='+server+';DATABASE='+bd+';UID='+usuario+';PWD='+contrasenia)
    print('Conexion exitosa')
except:
    print('Error al conectar con la base de datos')