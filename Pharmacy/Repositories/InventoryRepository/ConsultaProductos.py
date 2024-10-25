from Pharmacy.Repositories.InventoryRepository.ConexionCasera import conexion

#---------------------Mandar a llamar la tabla en consola--------------------
cursor=conexion.cursor()
cursor.execute("SELECT CodigoItem_Id, Nombre_Item,Descripcion_Item,CostoUnitario_Item,Imagen_Item,Tamano_Unidad FROM Producto.Items")

producto=cursor.fetchone()
while producto:
    print(producto)
    producto=cursor.fetchone()


cursor.close()
conexion.close()