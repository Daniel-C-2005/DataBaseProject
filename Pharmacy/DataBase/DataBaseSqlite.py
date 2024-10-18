import sqlite3

# Conectar a la base de datos (o crearla si no existe)
conexion = sqlite3.connect('usuarios.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conexion.cursor()

# Crear la tabla de usuarios si no existe
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_usuario TEXT NOT NULL UNIQUE,
    contrasena TEXT NOT NULL
)
''')

# Guardar los cambios y cerrar la conexión
conexion.commit()
conexion.close()

print("Base de datos creada exitosamente.")
