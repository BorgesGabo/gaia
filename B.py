def B():

    #las condiciones para el query ->DAL> query
    query = db.po.id==db.po_detail.po_id
    query &= db.po_detail.product_id==db.product.id
    query &= db.po.po_number<2428
    
    #obtiene el numero total de pedidos en el rango
    orders_in_range=db(query).select(db.po.id, groupby='po.po_number').as_list()
    n=len(orders_in_range)
    print str('orders id in range are:')
    print orders_in_range
    
    #d_list=db(query_name).select(db.customer.full_name, groupby='po.po_number').as_list()
    #print str('d_list is:')
    #print d_list

    #obtiene todos los productos contenidos en todos los pedidos sin repetir ->list> a_list
    a_list=db(query).select(db.product.id, groupby='product.name').as_list()
    '''print str('*')*30
    print str('a_list: all products id in query no repeated are:')
    print a_list'''
   
    b_list=[]
    c_list=[]
    d_list=[]
    addend_of_c_list=[]
    
    
    #obtiene el primer elemento de a_list -> DAL> query_ai
    for i in range(5):
        print str('*')*30
        print str('i-element of a_list is:')
        print i
        
        query_ai= query
        query_ai &= db.product.id==a_list[i]['id']
        print str('query_ai is:')
        print query_ai

        #obtiene todos los pedidos Ai-> lista> pedidos_ai_list, cuenta No pedidos no repetidos -> int> n, crea B ->lista>b_list
        pedidos_ai_list=db(query_ai).select(db.po.id, orderby='po.po_number', groupby='po.po_number').as_list()
        print str('*')*30
        print str('pedidos_ai_list: all the orders (ids) in range containing id of Ai element are:')
        print pedidos_ai_list
        
        #for e/a cada pedido del rango...
        for j in range(0,n):
            print str('+')*30
            print str('j is:')
            print j
            print str('+')*30
            print str('n is:')
            print n
            orders_in_range_j=orders_in_range[j]['id'] #obtenga el id del j-esimo pedido del rango
            print str('orders_in_range_j: is the j-esim order id:')
            print orders_in_range_j


            for k in range(len(pedidos_ai_list)): # for cada uno de los elementos en la lista de pedidos que tiene el producto ai
                print str('k is:')
                print k

                print str('pedidos_ai_list[k] is:')
                print pedidos_ai_list[k]
                if orders_in_range_j==pedidos_ai_list[k]['id']: # si el id del j-esimo pedido del coincide con id del pedido que tiene el ai... 
                    query_b = query_ai  #el nuevo constraint ... 
                    query_b &= db.po.id==pedidos_ai_list[k]['id'] # toma el pedido con cuyo id coincide con el del pedido que tiene producto ai
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
                    b_list.append(qty_bij*pres_bij) #multiplica los dos valores y agrega a la lista de b
                    addend_of_c_list.append(qty_bij*pres_bij) #multiplica los dos valores y  los agrega a la lista sumandos
                    print str('b_list is:')
                    print b_list

                else:         # si el pedido j-esimo no tiene productos en A:
                    print str('b_list is:')
                    print b_list
                    b_list.append(0)
                    addend_of_c_list.append(0)
                    print str('b_list is:')
                    print b_list
            
        
            if j==n-1: #en el ultimo loop de j
                print str('adddend of c are:')
                print addend_of_c_list
                c_list.append(sum(addend_of_c_list)) #obtiene la suma de las cantidades de los pedidos
                #reinicia todo a ceros
                del addend_of_c_list[:]
        #print str('c erased is:')
        print addend_of_c_list
    print str('total of products contained in the orders are:')
    print len(a_list)
    print str('c_list is:')
    print c_list
    print str('the c size is equal to the size of a_list?')+str('  ')+str(len(c_list)==len(a_list))
    
    
    query_name = query
    query_name &= db.po.customer_id==db.customer.id
    d_list=db(query_name).select(db.po.po_number, groupby='po.po_number').as_list()
    print str('d_list is:')
    print d_list
    print str('b_list:')
    print b_list
    '''print str('a_list is:')
    print a_list'''
    '''
    #************************************* IMPRIME TABLA RESUMEN **************************************
    a_names_lst=db(query).select(db.product.name, groupby='product.name').as_list()  #obtiene lista de nombres productos no repetidos en rango
    field_names_lst=[str(x['po_number']) for x in d_list ] #crea una lista con todos los numeros del pedido dentro del rango
    field_names_lst.insert(0, "Producto")                   # agrega al inicio de la lista el titulo producto 
    field_names_lst.insert(len(field_names_lst),"Total")    # Adiciona al final de la lista el titulo total
    summary_table=PrettyTable(field_names_lst)              # crea la tabla resumen con los titulos de cada columna
    total_lst=[]
    for y in range (0,len(a_list)):
        #print str('quantity is')
        begining_slice=y*n                                  #definicion del inicio del intervalo de corte de la lista
        end_slice=begining_slice+n                          #definicion del fin del intervalo de corte de la lista
        row_summary_lst=b_list[begining_slice:end_slice]    #Toma los totales entre el incio y fin del intervalo sin tocar el fin
        #total=sum(row_summary_lst)                      #suma las cantidades de todos los pedidos del rango
        row_summary_lst.insert(0,a_names_lst[y]['name'])    #agrega el nombre al inicio de la lista
        row_summary_lst.insert(len(row_summary_lst),c_list[y])  #agrega el total al final de la lista
        #row_summary_lst.insert(len(row_summary_lst),total)  # agrega el total al final de la lista
        summary_table.add_row(row_summary_lst)              # agrega filas a la tabla
        summary_table.align['Producto']='l'                 # alinea la a la izquierda la primera columna
        
        #print row_summary_lst  '''
        
    '''
    
    def summary (query, b_list, c_list, d_list):
        a_list_as_names=db(query).select(db.product.name, groupby='product.name').as_list()
        x=PrettyTable(["Productos"])
        print str('a_list_as_names are:')
        print a_list_as_names
        for a in a_list_as_names:
            b=a['name']
            x.add_row([b])
            x.align["Productos"]="l"
            #x.hrules = prettytable.ALL
            
        print str('summary table is:')
        print x
        return
    summary(query, b_list, c_list, d_list)'''
    
    #print str('the summary table is:')
    #print summary_table
    return 
