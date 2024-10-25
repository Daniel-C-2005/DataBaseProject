from itertools import product

from Pharmacy.Repositories.ProductService.ConexionCasera import conexion


#---------------------Mandar a llamar la tabla en consola--------------------
#cursor=conexion.cursor()
#cursor.execute("Select*From Producto.Items;")

#producto=cursor.fetchone()
#while producto:
#    print(producto)
#    producto=cursor.fetchone()


#producto=cursor.fetchall()
#for producto in producto:
#    print(producto)

#cursor.close()

#-------------------Insert-----------------------
cursorinsert=conexion.cursor()
insertar=("Insert into Producto.Items(Nombre_Item,Descripcion_Item,CostoUnitario_Item,Imagen_Item,Descuento_Id,Presentacion_Id,"
          "Tamano_Unidad,UnidadMedida_Id,Categoria_Id) values (?,?,?,?,?,?,?,?,?);")

#Ingresar datos Nixon con los textfield supongo
##cursorinsert.execute(insertar,Parametro,Parametro,Parametro,Parametro,Parametro,Parametro,Parametro,Parametro,Parametro)


cursorinsert.commit()
cursorinsert.close()

#-----------------Update-----------------------

cursorupdate=conexion.cursor()
actualizar="Update Producto.Items set Descripcion_Item=?,CostoUnitario_Item=?,Imagen_Item=?,Descuento_Id=?,Presentacion_Id=?,Tamano_Unidad=?,UnidadMedida_Id=?,Categoria_Id=? where Nombre_Item=?"

#Ingresar los datos para actualizar la fila del nombre seleccionado
#cursorupdate.execute(actualizar,Parametro,Parametro,Parametro,Parametro,Parametro,Parametro,Parametro,Parametro,ParametroName)

cursorupdate.commit()
cursorupdate.close()

#-----------------find----------------------------

cursorfind=conexion.cursor()
buscar="Select * From Producto.Items where CodigoItem_Id=?"

#Ingresar el Id para encontrar la fila seleccionada
#cursorfind.execute(buscar,Parametro)

print(cursorfind.fetchall())
cursorfind.close()

#-----------------Delete--------------------------

cursordelete=conexion.cursor()
eliminar="delete from Producto.Items where CodigoItem_Id=?"

#Ingresar el Id para eliminar la fila seleccionada
#cursordelete.execute(eliminar,Parametro)

cursordelete.commit()
cursordelete.close()


#--------------------Tabla actualizada en consola-------------------
#print("-----------------------------------------------------------")
#cursorc=conexion.cursor()
#cursorc.execute("Select * From Producto.Items;")
#productos=cursorc.fetchall()
#for producto in productos:
#    print(producto)

#cursorc.close()
#conexion.close()


