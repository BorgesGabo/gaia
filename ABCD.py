def ABCD():

    b_lst=[]                                                                       #crea lista de b con los subtotales
    c_lst=[]                                                                       #crea lista de c contiene los totales por producto
    
    #******************************QUERY BASE **************************************

    #define el query base -> DAL > query
    query = db.po.id==db.po_detail.po_id                   
    query &= db.po_detail.product_id==db.product.id
    query &= db.po.po_number<2428

    orders_query_lst=db(query).select(db.po.id, db.po.po_number, groupby='po.po_number').as_list()   #obtiene id de los pedidos del query
    n=len(orders_query_lst)                                                                         #obtiene el numero de pedidos de query
    d_lst=[x['id'] for x in orders_query_lst]                                                        #obtiene las referencias de los pedidos del query
    #print orders_query_lst 
    #print '\n'
    #print d_lst

    #******************************QUERY A *****************************************
    a_products_lst=db(query).select(db.product.id, db.product.name, groupby='product.name').as_list() # obtiene id y nombre de productos del query sin repetir


    for i in range (5):                                                                        # iterando sobre a_products_lst

        query_a = query    
        query_a &= db.product.id==a_products_lst[i]['id']
        a_orders_lst = db(query_a).select(db.po.id, orderby='po.po_number', groupby='po.po_number').as_list() #obtiene los id de pedidos que tienen ese producto
        
  
        print a_orders_lst
    print '\n'
    #print a_
