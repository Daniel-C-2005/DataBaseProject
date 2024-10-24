# import pyodbc
# from fpdf import FPDF
#
#
# # Configurar conexión usando la clase de conexión proporcionada
# class ConexionCasera:
#     def __init__(self):
#         self.server = 'localhost'
#         self.bd = 'Db_ProyectoDB1_1'
#         self.usuario = 'soporte'
#         self.contrasenia = '123'
#
#     def conectar(self):
#         try:
#             conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
#                                       'SERVER=' + self.server + ';'
#                                                                 'DATABASE=' + self.bd + ';'
#                                                                                         'UID=' + self.usuario + ';'
#                                                                                                                 'PWD=' + self.contrasenia)
#             print('Conexion exitosa')
#             return conexion
#         except Exception as e:
#             print('Error al conectar con la base de datos:', e)
#             return None
#
#
# # Crear una instancia de la clase de conexión
# conexion_casera = ConexionCasera()
# conn = conexion_casera.conectar()
#
# # Verificar si la conexión fue exitosa antes de continuar
# if conn:
#     cursor = conn.cursor()
#
#     # Ejecutar el query
#     query = '''
#     WITH ProductosUnicos AS (
#         SELECT
#             I.CodigoItem_Id AS 'Codigo producto',
#             I.Nombre_Item AS 'Nombre Producto',
#             CAST(F.CantidadExist AS INT) AS 'Cantidad de Producto',
#             I.CostoUnitario_Item AS 'Costo Unitario',
#             F.PrecioVenta AS 'Precio Venta',
#             ROW_NUMBER() OVER (PARTITION BY I.Nombre_Item ORDER BY I.CodigoItem_Id) AS RowNum
#         FROM
#             Producto.Items I
#         JOIN
#             Farmacia.Inventario F ON I.CodigoItem_Id = F.CodigoItem_Id
#     )
#     SELECT
#         [Codigo producto],
#         [Nombre Producto],
#         [Cantidad de Producto],
#         [Costo Unitario],
#         [Precio Venta]
#     FROM
#         ProductosUnicos
#     WHERE
#         RowNum = 1
#     ORDER BY
#         [Codigo Producto] ASC;
#     '''
#
#     cursor.execute(query)
#     results = cursor.fetchall()
#
#     # Cerrar la conexión
#     conn.close()
#
#     # Crear un PDF
#     pdf = FPDF(orientation='P', unit='mm', format='Letter')
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()
#
#     pdf.image('Log.jpg', x=3, y=1, w=10, h=10)
#
#     # Agregar título
#     pdf.set_font('Arial', 'B', 14)
#     pdf.cell(200, 10, 'Reporte', ln=True, align='C')
#     pdf.set_fill_color(200, 200, 200)
#     # Agregar encabezados de la tabla
#     pdf.set_font('Arial', 'B', 12)
#     pdf.cell(40, 10, 'Codigo Producto', 1, 0, 'C', 1)
#     pdf.cell(60, 10, 'Nombre Producto', 1, 0, 'C', 1)
#     pdf.cell(40, 10, 'Cantidad Producto', 1, 0, 'C', 1)
#     pdf.cell(30, 10, 'Costo Unitario', 1, 0, 'C', 1)
#     pdf.cell(30, 10, 'Precio Venta', 1, 1, 'C', 1)
#
#     # Agregar filas de resultados
#     pdf.set_font('Arial', '', 12)
#     pdf.set_fill_color(220, 255, 220)
#     for row in results:
#         pdf.cell(40, 8, str(row[0]), 1, 0, 'C', 1)
#         pdf.cell(60, 8, str(row[1]), 1, 0, 'C', 1)
#         pdf.cell(40, 8, str(row[2]), 1, 0, 'C', 1)
#         pdf.cell(30, 8, f"{row[3]:.2f}", 1, 0, 'C', 1)  # Muestra el costo unitario con dos decimales
#         pdf.cell(30, 8, f"{row[4]:.2f}", 1, 1, 'C', 1)  # Muestra el precio de venta con dos decimales
#
#     # Guardar el PDF
#     pdf_output_path = 'Reporte Farmacia.pdf'
#     pdf.output(pdf_output_path)
#
#     print(f'PDF generado correctamente: {pdf_output_path}')
# else:
#     print('No se pudo realizar la conexión a la base de datos, por lo que no se pudo generar el PDF.')

import pyodbc
from fpdf import FPDF

# Conexión a la base de datos
server = 'localhost'
bd = 'Db_ProyectoDB1_1'
usuario = 'soporte'
contrasenia = '123'

try:
    conexion = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=' + server + ';'
        'DATABASE=' + bd + ';'
        'UID=' + usuario + ';'
        'PWD=' + contrasenia)
    print('Conexión exitosa')
except:
    print('Error al conectar con la base de datos')


# Consulta SQL con las nuevas columnas Bodega y Estantería
query = """
SELECT DISTINCT
    I.CodigoItem_Id AS 'Codigo producto',
    I.Nombre_Item AS 'Nombre Producto',
    F.CantidadExist AS 'Cantidad de Producto',
    I.CostoUnitario_Item AS 'Costo Unitario',
    F.PrecioVenta AS 'Precio Venta',
    B.Nombre_Bodega AS 'Nombre Bodega',
    BE.Estanteria_Id AS 'Estantería'
FROM 
    Producto.Items I
JOIN 
    Farmacia.Inventario F ON I.CodigoItem_Id = F.CodigoItem_Id
JOIN 
    Farmacia.BodegaEstanterias BE ON F.BodegaEsta_Id = BE.BodegaEstanteria_Id
JOIN 
    Farmacia.Bodega B ON BE.Bodega_Id = B.Bodega_Id
ORDER BY 
    I.CodigoItem_Id ASC;
"""

# Ejecutar consulta
cursor = conexion.cursor()
cursor.execute(query)
resultados = cursor.fetchall()

# Crear un nuevo PDF
pdf = FPDF(orientation='L', unit='mm', format='A4')
pdf.add_page()

pdf.image('Log.jpg', x=3, y=1, w=10, h=10)

pdf.set_font('Times', 'B', 20)
pdf.cell(270, 10, 'Reporte', ln=True, align='C')

# Configuración de colores y encabezados
pdf.set_font('Arial', 'B', 12)

# Color de fondo del encabezado
pdf.set_fill_color(200, 200, 200)  # gris claro
pdf.cell(40, 10, 'Codigo producto', 1, 0, 'C', 1)
pdf.cell(50, 10, 'Nombre Producto', 1, 0, 'C', 1)
pdf.cell(55, 10, 'Cantidad de Producto', 1, 0, 'C', 1)
pdf.cell(30, 10, 'Costo Unitario', 1, 0, 'C', 1)
pdf.cell(30, 10, 'Precio Venta', 1, 0, 'C', 1)
pdf.cell(40, 10, 'Nombre Bodega', 1, 0, 'C', 1)
pdf.cell(30, 10, 'Estantería', 1, 1, 'C', 1)

# Colores para las filas
pdf.set_font('Arial', '', 10)

# Rellenar filas
for idx, row in enumerate(resultados):
    # Color de fondo verde pastel para las filas
    if idx % 2 == 0:
        pdf.set_fill_color(144, 238, 144)  # verde pastel

    pdf.cell(40, 10, str(row[0]), 1, 0, 'C', 1)
    pdf.cell(50, 10, row[1], 1, 0, 'C', 1)
    pdf.cell(55, 10, str(row[2]), 1, 0, 'C', 1)
    pdf.cell(30, 10, str(row[3]), 1, 0, 'C', 1)
    pdf.cell(30, 10, str(row[4]), 1, 0, 'C', 1)
    pdf.cell(40, 10, row[5], 1, 0, 'C', 1)
    pdf.cell(30, 10, str(row[6]), 1, 1, 'C', 1)

# Guardar el archivo PDF
pdf_file_name = "reporte_inventario_bodega.pdf"
pdf.output(pdf_file_name)

# Verificar si el archivo fue guardado correctamente
import os
if os.path.exists(pdf_file_name):
    print(f"PDF guardado correctamente como {pdf_file_name}")
else:
    print("Error al guardar el archivo PDF.")

