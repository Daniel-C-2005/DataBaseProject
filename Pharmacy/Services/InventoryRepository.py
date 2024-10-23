from Pharmacy.Repositories.InventoryRepository.ConexionCasera import conexion

#-------------------------------------

#Validar el parametro a ingresar
nuevaCantidad=int
if nuevaCantidad < 0:
    raise ValueError("La cantidad de stock no puede ser negativa.")
if nuevaCantidad <= 0 or nuevaCantidad > 10000:
    raise ValueError("El precio de venta debe ser mayor que 0 y menor que 10,000.")

cursorupdate=conexion.cursor()
actualizar="Update Farmacia.Inventario set CantidadExist=?,PrecioVenta=? where Inventario_Id=?"

#Ingresar los datos para actualizar la fila del nombre seleccionado
#cursorupdate.execute(actualizar,Parametro,Parametro,ParametroInventario_Id)

cursorupdate.commit()
cursorupdate.close()
conexion.close()

