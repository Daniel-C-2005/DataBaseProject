#-------------Estado actual del inventario, incluyendo cantidad y productos relacionados---------------
from fpdf import FPDF

from Pharmacy.Repositories.InventoryRepository.ConexionCasera import conexion
InventarioPDF = conexion.cursor()
InventarioPDF.execute("SELECT i.CodigoItem_Id,p.Nombre_Item, i.BodegaEsta_Id, i.CantidadExist, i.PrecioVenta FROM Farmacia.Inventario as i JOIN Producto.Items as p ON i.CodigoItem_Id = p.CodigoItem_Id;")


results = InventarioPDF.fetchall()

InventarioPDF.close()

# Crear un PDF
pdf = FPDF(orientation='P', unit='mm', format='Letter')
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()


# Agregar título
pdf.set_font('Arial', 'B', 14)
pdf.cell(200, 10, 'Estado del inventario', ln=True, align='C')
pdf.set_fill_color(200, 200, 200)
# Agregar encabezados de la tabla
pdf.set_font('Arial', 'B', 12)
pdf.cell(40, 10, 'Codigo Producto', 1, 0, 'C', 1)
pdf.cell(60, 10, 'Nombre Producto', 1, 0, 'C', 1)
pdf.cell(40, 10, 'Bodega Estado Id', 1, 0, 'C', 1)
pdf.cell(30, 10, 'Cantidad Exist', 1, 0, 'C', 1)
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
