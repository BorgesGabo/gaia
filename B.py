def B():

  #las condiciones para el query ->DAL> query
  query = db.po.id==db.po_detail.po_id
  query &= db.po_detail.product_id==db.product.id
  query &= db.po.po_number<2430

  #obtiene todos los productos contenidos en todos los pedidos sin repetir ->list> a_list
  a_list=db(query).select(db.product.id, groupby='product.name').as_list()
  print str('A is:')
  print A

  #filtra los del primer producto de A -> DAL> query_a
  query_ai= query
  query_ai &= a_list[0]['id']

  #obtiene todos los pedidos Ai-> lista> pedidos_ai_list, cuenta No pedidos -> int> n, crea B ->lista>b_list
  pedidos_ai_list=db(query_ai).select(db.po.id orderby=db.po.po_number).as_list()
  n=len(pedidos_ai_list)
  b_list=[]
#for e/a cada pedido...
for j in range(0,n):
  if len(pedidos_ai_list[j])== 0: #si el pedido j es un elemento vacio
    b_list[j]=0 #asignele un cero
  else:         # en caso contrario
    query_b &= query_ai  #el nuevo constraint ... 
    query_b &= db.po.id==pedidos_ai_list[j] # toma el pedido con id igual al j-esimo pedido de la lista
    #b_list[j]=int(db(query_b).select(db.product.pres))*int(db(query_b).select(db.po_detail.quantity))
    qty_bij=int(db(query_b).select(db.product.pres)) #obtiene el entero de la presentacion
    pres_bij=int(db(query_b).select(db.po_detail.quantity)) #obtiene el entero de la cantidad
    b_list.append(qty_bij*pres_bij) #multiplica los dos valores y agrega a la lista


return dict()
