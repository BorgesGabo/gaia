def B():

    #las condiciones para el query ->DAL> query
    query = db.po.id==db.po_detail.po_id
    query &= db.po_detail.product_id==db.product.id
    query &= db.po.po_number<2430
    
    #obtiene el numero total de pedidos en el rango
    orders_in_range=db(query).select(db.po.id, groupby='po.po_number').as_list()
    n=len(orders_in_range)
    print str('orders in range are:')
    print orders_in_range

    #obtiene todos los productos contenidos en todos los pedidos sin repetir ->list> a_list
    a_list=db(query).select(db.product.id, groupby='product.name').as_list()
    print str('a_list is:')
    print a_list
    
    #obtiene el primer elemento de a_list -> DAL> query_ai
    query_ai= query
    query_ai &= db.product.id==a_list[0]['id']
    print str('query_ai is:')
    print query_ai

    #obtiene todos los pedidos Ai-> lista> pedidos_ai_list, cuenta No pedidos no repetidos -> int> n, crea B ->lista>b_list
    pedidos_ai_list=db(query_ai).select(db.po.id, orderby='po.po_number', groupby='po.po_number').as_list()
    print str('pedidos_ai_list is:')
    print pedidos_ai_list
    b_list=[]

    #for e/a cada pedido del rango...
    for j in range(0,n):
        print str('j is:')
        print j
        orders_in_range_j=orders_in_range[j]['id'] #obtenga el id del j-esimo pedido del rango
        print str('orders_in_range_j is:')
        print orders_in_range_j
        
        
        for k in range(len(pedidos_ai_list)):
            print str('k is:')
            print k
            
            print str('pedidos_ai_list[k] is:')
            print pedidos_ai_list[k]
            if orders_in_range_j==pedidos_ai_list[k]['id']: 
                query_b = query_ai  #el nuevo constraint ... 
                query_b &= db.po.id==pedidos_ai_list[k]['id'] # toma el pedido con id igual al j-esimo pedido de la lista devuelve el id
                print str('query_b is:')
                print query_b
        #if orders_in_range_j in pedidos_ai_list:
        #if any(d['id']==orders_in_range_j for d in pedidos_ai_list):
                qty_bij=int(db(query_b).select(db.product.pres).as_list()[0]['pres']) #obtiene el entero de la presentacion
                print str('qty_bij is:')
                print qty_bij
                pres_bij=int(db(query_b).select(db.po_detail.quantity).as_list()[0]['quantity']) #obtiene el entero de la cantidad
                print str('pres_bij is:')
                print pres_bij
                b_list.append(qty_bij*pres_bij) #multiplica los dos valores y agrega a la lista
                print str('b_list is:')
                print b_list

            else:         # en caso contrario
                print str('b_list is:')
                print b_list
                b_list.append(0)
                print str('b_list is:')
                print b_list

    
    return 
