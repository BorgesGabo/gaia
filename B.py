def B():

query...

#filtra los del primer producto de A -> DAL> query_A
query_A= query
query_A &= A[0]['id']

#obtiene todos los pedidos-> lista> pedidos_lst, cuenta No pedidos -> int> n
pedidos_lst=db(query_A).select(db.po.id orderby=db.po.po_number).as_list()
n=len(pedidos_lst)
#for e/a pedido busca po_detail.quantity(j) si es vacio ponga '0' else product.pres(j)*po_detail.quantity(j) ->B
#cada loop append-> B

query_B=query
query_B=db().select()
for j in range (0, n):
  

return dic()
