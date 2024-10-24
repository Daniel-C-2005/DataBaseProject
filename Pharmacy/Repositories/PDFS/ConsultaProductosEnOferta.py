from fpdf import FPDF

from Pharmacy.Repositories.InventoryRepository.ConexionCasera import conexion

OfertaPDF=conexion.cursor()
OfertaPDF.execute("SELECT p.Nombre_Item,p.Descripcion_Item,p.CostoUnitario_Item,d.Descuento_Porcentual FROM Producto.Items as p JOIN Producto.Descuentos as d ON p.Descuento_Id = d.Descuento_Id "
                        "WHERE d.Descuento_Porcentual > 0;")

results=OfertaPDF.fetchall()

OfertaPDF.close()

# Crear un PDF
pdf = FPDF(orientation='P', unit='mm', format='Letter')
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()


# Agregar título
pdf.set_font('Arial', 'B', 14)
pdf.cell(200, 10, 'Productos En Oferta', ln=True, align='C')
pdf.set_fill_color(200, 200, 200)
# Agregar encabezados de la tabla
pdf.set_font('Arial', 'B', 12)
pdf.cell(50, 10, 'Nombre', 1, 0, 'C', 1)
pdf.cell(70, 10, 'Descripcion', 1, 0, 'C', 1)
pdf.cell(40, 10, 'Costo Unitario', 1, 0, 'C', 1)
pdf.cell(45, 10, 'Descuento Porcentual', 1, 0, 'C', 1)

# Agregar filas de resultados
pdf.set_font('Arial', '', 12)
pdf.set_fill_color(220, 255, 220)
for row in results:
    pdf.cell(200, 8, '', ln=True, align='C')
    pdf.cell(50, 8, str(row[0]), 1, 0, 'C', 1)
    pdf.cell(70, 8, str(row[1]), 1, 0, 'C', 1)
    pdf.cell(40, 8, f"{row[2]:.2f}", 1, 0, 'C', 1)  # Muestra el costo unitario con dos decimales
    pdf.cell(45, 8, f"{row[3]:.2f}", 1, 0, 'C', 1)  # Muestra el costo unitario con dos decimales

# Guardar el PDF
pdf_output_path = 'Reporte Farmacia.pdf'
pdf.output(pdf_output_path)

print(f'PDF generado correctamente: {pdf_output_path}')