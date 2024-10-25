from Pharmacy.Repositories.InventoryRepository.ConexionCasera import conexion

#-------------Estado actual del inventario, incluyendo cantidad y productos relacionados---------------
InventarioEstado=conexion.cursor()
InventarioEstado.execute("SELECT i.CodigoItem_Id,p.Nombre_Item, i.BodegaEsta_Id, i.CantidadExist, i.PrecioVenta FROM Farmacia.Inventario as i "
           "JOIN Producto.Items as p ON i.CodigoItem_Id = p.CodigoItem_Id;")

coso=InventarioEstado.fetchone()
while coso:
    print(coso)
    coso=InventarioEstado.fetchone()

InventarioEstado.close()
print("")
#--------------------------Productos agotados-----------------------------------

ProductosAgotados=conexion.cursor()
ProductosAgotados.execute("SELECT p.Nombre_Item,p.Descripcion_Item,p.CostoUnitario_Item FROM Farmacia.Inventario as i JOIN Producto.Items as p ON i.CodigoItem_Id = p.CodigoItem_Id "
                          "WHERE i.CantidadExist=0")

coso=ProductosAgotados.fetchone()
while coso:
    print(coso)
    coso=ProductosAgotados.fetchone()

ProductosAgotados.close()
print("")

#--------------------Productos en oferta------------------------------------------

ProductosOferta=conexion.cursor()
ProductosOferta.execute("SELECT p.Nombre_Item,p.Descripcion_Item,p.CostoUnitario_Item,d.Descuento_Porcentual FROM Producto.Items as p JOIN Producto.Descuentos as d ON p.Descuento_Id = d.Descuento_Id "
                        "WHERE d.Descuento_Porcentual > 0;")

coso=ProductosOferta.fetchone()
while coso:
    print(coso)
    coso=ProductosOferta.fetchone()

ProductosOferta.close()

conexion.close()
