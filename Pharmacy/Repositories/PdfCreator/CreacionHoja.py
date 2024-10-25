import pyodbc
from fpdf import FPDF
import os

class PDFReportGenerator:
    def __init__(self, server, bd, usuario, contrasenia):
        self.server = server
        self.bd = bd
        self.usuario = usuario
        self.contrasenia = contrasenia
        self.conexion = None

    def conectar_bd(self):
        try:
            self.conexion = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=' + self.server + ';'
                'DATABASE=' + self.bd + ';'
                'UID=' + self.usuario + ';'
                'PWD=' + self.contrasenia)
            print('Conexión exitosa')
        except Exception as e:
            print(f'Error al conectar con la base de datos: {e}')

    def ejecutar_consulta(self):
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
        cursor = self.conexion.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def generar_pdf(self, resultados, pdf_file_name):
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.add_page()

        pdf.image('2.png', x=3, y=1, w=20, h=20)

        pdf.set_font('Times', 'B', 20)
        pdf.cell(270, 10, 'Reporte', ln=True, align='C')

        pdf.set_font('Arial', 'B', 12)
        pdf.set_fill_color(200, 200, 200)
        pdf.cell(40, 10, 'Codigo producto', 1, 0, 'C', 1)
        pdf.cell(50, 10, 'Nombre Producto', 1, 0, 'C', 1)
        pdf.cell(55, 10, 'Cantidad de Producto', 1, 0, 'C', 1)
        pdf.cell(30, 10, 'Costo Unitario', 1, 0, 'C', 1)
        pdf.cell(30, 10, 'Precio Venta', 1, 0, 'C', 1)
        pdf.cell(40, 10, 'Nombre Bodega', 1, 0, 'C', 1)
        pdf.cell(30, 10, 'Estantería', 1, 1, 'C', 1)

        pdf.set_font('Arial', '', 10)
        for idx, row in enumerate(resultados):
            if idx % 2 == 0:
                pdf.set_fill_color(144, 238, 144)
            pdf.cell(40, 10, str(row[0]), 1, 0, 'C', 1)
            pdf.cell(50, 10, row[1], 1, 0, 'C', 1)
            pdf.cell(55, 10, str(row[2]), 1, 0, 'C', 1)
            pdf.cell(30, 10, str(row[3]), 1, 0, 'C', 1)
            pdf.cell(30, 10, str(row[4]), 1, 0, 'C', 1)
            pdf.cell(40, 10, row[5], 1, 0, 'C', 1)
            pdf.cell(30, 10, str(row[6]), 1, 1, 'C', 1)

        pdf.output(pdf_file_name)

        if os.path.exists(pdf_file_name):
            print(f"PDF guardado correctamente como {pdf_file_name}")
        else:
            print("Error al guardar el archivo PDF.")

# Ejemplo de uso
if __name__ == '__main__':
    server = 'DANIEL\\MSSQLSERVER01'
    bd = 'Db_ProyectoDB1_1'
    usuario = 'soporte'
    contrasenia = '123'

    pdf_generator = PDFReportGenerator(server, bd, usuario, contrasenia)
    pdf_generator.conectar_bd()
    resultados = pdf_generator.ejecutar_consulta()
    pdf_generator.generar_pdf(resultados, "reporte_inventario_bodega.pdf")