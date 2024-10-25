#--------------------------Productos agotados-----------------------------------
from math import trunc

from fpdf import FPDF

from Pharmacy.Repositories.InventoryRepository.ConexionCasera import conexion

AgotadosPDF = conexion.cursor()
AgotadosPDF.execute("SELECT p.Nombre_Item as 'Nombre Producto',p.Descripcion_Item as 'Descripcion',p.CostoUnitario_Item as 'Costo Unitario' FROM Farmacia.Inventario as i JOIN Producto.Items as p ON i.CodigoItem_Id = p.CodigoItem_Id WHERE i.CantidadExist=0")


results = AgotadosPDF.fetchall()

AgotadosPDF.close()

# Crear un PDF
pdf = FPDF(orientation='P', unit='mm', format='Letter')
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()


# Agregar título
pdf.set_font('Arial', 'B', 14)
pdf.cell(200, 10, 'Productos Agotados', ln=True, align='C')
pdf.set_fill_color(200, 200, 200)

# Agregar encabezados de la tabla
pdf.set_font('Arial', 'B', 12)
pdf.cell(40, 10, 'Nombre Producto', 1, 0, 'C', 1)
pdf.cell(60, 10, 'Descripcion', 1, 0, 'C', 1)
pdf.cell(40, 10, 'Costo Unitario', 1, 0, 'C', 1)


# Agregar filas de resultados
pdf.set_font('Arial', '', 12)
pdf.set_fill_color(220, 255, 220)
for row in results:
    pdf.cell(200, 8, '', ln=True, align='C')
    pdf.cell(40, 8, str(row[0]), 1, 0, 'C', 1)
    pdf.cell(60, 8, str(row[1]), 1, 0, 'C', 1)
    pdf.cell(40, 8, f"{row[2]:.2f}", 1, 0, 'C', 1)  # Muestra el costo unitario con dos decimales

# Guardar el PDF
pdf_output_path = 'Reporte Farmacia.pdf'
pdf.output(pdf_output_path)

print(f'PDF generado correctamente: {pdf_output_path}')