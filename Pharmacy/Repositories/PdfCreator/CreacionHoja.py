import pyodbc
from fpdf import FPDF


# Configurar conexión usando la clase de conexión proporcionada
class ConexionCasera:
    def __init__(self):
        self.server = 'localhost'
        self.bd = 'Db_ProyectoDB1_1'
        self.usuario = 'soporte'
        self.contrasenia = '123'

    def conectar(self):
        try:
            conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                                      'SERVER=' + self.server + ';'
                                                                'DATABASE=' + self.bd + ';'
                                                                                        'UID=' + self.usuario + ';'
                                                                                                                'PWD=' + self.contrasenia)
            print('Conexion exitosa')
            return conexion
        except Exception as e:
            print('Error al conectar con la base de datos:', e)
            return None


# Crear una instancia de la clase de conexión
conexion_casera = ConexionCasera()
conn = conexion_casera.conectar()

# Verificar si la conexión fue exitosa antes de continuar
if conn:
    cursor = conn.cursor()

    # Ejecutar el query
    query = '''
    WITH ProductosUnicos AS (
        SELECT 
            I.CodigoItem_Id AS 'Codigo producto',
            I.Nombre_Item AS 'Nombre Producto',
            CAST(F.CantidadExist AS INT) AS 'Cantidad de Producto', 
            I.CostoUnitario_Item AS 'Costo Unitario',
            F.PrecioVenta AS 'Precio Venta',
            ROW_NUMBER() OVER (PARTITION BY I.Nombre_Item ORDER BY I.CodigoItem_Id) AS RowNum
        FROM 
            Producto.Items I
        JOIN 
            Farmacia.Inventario F ON I.CodigoItem_Id = F.CodigoItem_Id
    )
    SELECT 
        [Codigo producto],
        [Nombre Producto],
        [Cantidad de Producto],
        [Costo Unitario],
        [Precio Venta]
    FROM 
        ProductosUnicos
    WHERE 
        RowNum = 1
    ORDER BY 
        [Codigo Producto] ASC;
    '''

    cursor.execute(query)
    results = cursor.fetchall()

    # Cerrar la conexión
    conn.close()

    # Crear un PDF
    pdf = FPDF(orientation='P', unit='mm', format='Letter')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.image('Log.jpg', x=3, y=1, w=10, h=10)

    # Agregar título
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(200, 10, 'Reporte', ln=True, align='C')
    pdf.set_fill_color(200, 200, 200)
    # Agregar encabezados de la tabla
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, 'Codigo Producto', 1, 0, 'C', 1)
    pdf.cell(60, 10, 'Nombre Producto', 1, 0, 'C', 1)
    pdf.cell(40, 10, 'Cantidad Producto', 1, 0, 'C', 1)
    pdf.cell(30, 10, 'Costo Unitario', 1, 0, 'C', 1)
    pdf.cell(30, 10, 'Precio Venta', 1, 1, 'C', 1)

    # Agregar filas de resultados
    pdf.set_font('Arial', '', 12)
    pdf.set_fill_color(220, 255, 220)
    for row in results:
        pdf.cell(40, 8, str(row[0]), 1, 0, 'C', 1)
        pdf.cell(60, 8, str(row[1]), 1, 0, 'C', 1)
        pdf.cell(40, 8, str(row[2]), 1, 0, 'C', 1)
        pdf.cell(30, 8, f"{row[3]:.2f}", 1, 0, 'C', 1)  # Muestra el costo unitario con dos decimales
        pdf.cell(30, 8, f"{row[4]:.2f}", 1, 1, 'C', 1)  # Muestra el precio de venta con dos decimales

    # Guardar el PDF
    pdf_output_path = 'Reporte Farmacia.pdf'
    pdf.output(pdf_output_path)

    print(f'PDF generado correctamente: {pdf_output_path}')
else:
    print('No se pudo realizar la conexión a la base de datos, por lo que no se pudo generar el PDF.')
