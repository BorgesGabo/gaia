def ABCD():

    b_lst=[]                                                                       #crea lista de b con los subtotales
    c_lst=[]                                                                       #crea lista de c contiene los totales por producto
    qty_lst=[]                                                                     #crea lista de cantidades
    pres_lst=[]                                                                     #crea lista de presentaciones
    #**************************************QUERY BASE **************************************
    #define el query base -> DAL > query
    query = db.po.id==db.po_detail.po_id
    query &= db.po_detail.product_id==db.product.id
    query &= db.po.po_number<2432

    orders_query_lst=db(query).select(db.po.id, db.po.po_number, groupby='po.po_number').as_list() #obtiene id de los pedidos del query
    n=len(orders_query_lst)                                                                      #obtiene el numero de pedidos de query
    d_lst=[str(x['po_number'])+'|Recibido' for x in orders_query_lst]                   #obtiene las referencias de los pedidos del query
    #print orders_query_lst                                                                 #impresion de prueba
    print '\n'
    #print d_lst                                                                            #impresion de prueba
    
    #***************************************QUERY A,B *****************************************
    a_product_id_lst=db(query).select(db.product.id, db.product.name, groupby='product.name').as_list() # obtiene id, nombre productos query sin repetir
    for i in range (len(a_product_id_lst)):                                                  # iterando sobre A: a_products_lst
        query_a = query
        query_a &= db.product.id==a_product_id_lst[i]['id']
        for j in range (n):                                              # iterando sobre orders_query_lst
            query_b = query_a
            query_b &= db.po.id ==orders_query_lst[j]['id']
            #print query_b                                               # impresion de prueba
            bj_lst = db(query_b).select(db.po_detail.quantity, orderby='po.po_number', groupby='po.po_number').as_list() #obtiene cantidad
            qtyj_lst = db(query_b).select(db.po_detail.quantity, orderby='po.po_number', groupby='po.po_number').as_list() #obtiene cantidad
            presj_lst =db(query_b).select(db.product.pres, orderby='po.po_number', groupby='po.po_number').as_list() #obtiene pres
            if len(bj_lst)==0:                                           #si el pedido no tiene este producto ponga 0
                bj_lst = 0
                b_lst.append(0)
            else:
                b_lst.append(int(bj_lst[0]['quantity']))                 # de lo contrario ponga el valor de bj_lst

            if len(qtyj_lst)==0:                                         #si no hay cantidad en ese pedido ponga un cero
                qtyj_lst=0
                presj_lst=0                                              #ponga un cero en la presentacion
                qty_lst.append(0)                                        #ingreselo en la lista de cantidad
                pres_lst.append(0)                                       #ingreselo en la lista de presentacion
            else:                                                        # en caso contrario obtenga los valores de la consultas
                qty_lst.append(int(qtyj_lst[0]['quantity']))             # obtiene el numero de cantidad
                pres_lst.append(int(presj_lst[0]['pres']))               # obtiene el numero de la presentacion del producto
    #print qty_lst                                                       #impresion de prueba
    #print pres_lst                                                      #impresion de prueba
    z_lst=[]
    z_lst=[qty_lst*pres_lst for qty_lst,pres_lst in zip(qty_lst,pres_lst)] #calcula pres*qty para cada uno de los elementos de la lista
    #print z_lst
            #print (str('j is:'), j)                                     #impresion de prueba
            #print (str('bj_lst is:'), bj_lst)                           #impresion de prueba
            #print (str('b_lst is:'), b_lst)                             #impresion de prueba

    #************************************* IMPRIME TABLA RESUMEN **************************************
    a_product_name_lst=db(query).select(db.product.name, groupby='product.name').as_list()  #obtiene lista de nombres productos no repetidos en rango
    field_names_lst=d_lst #crea una lista con todos los numeros del pedido dentro del rango
    field_names_lst.insert(0, "Producto")                   # agrega al inicio de la lista el titulo producto 
    field_names_lst.insert(len(field_names_lst),"Total")    # Adiciona al final de la lista el titulo total
    summary_table=PrettyTable(field_names_lst)              # crea la tabla resumen con los titulos de cada columna
    total_lst=[]
    for y in range (0,len(a_product_id_lst)):
        begining_slice=y*n                                  #definicion del inicio del intervalo de corte de la lista
        end_slice=begining_slice+n                          #definicion del fin del intervalo de corte de la lista
        row_summary_lst=z_lst[begining_slice:end_slice]     #Toma los totales entre el incio y fin del intervalo sin tocar el fin
                                                            #si desea solo las cantidades del pedido sin multiplicar por los pesos usar b_lst por Z_lst
        total=sum(row_summary_lst)                          #suma las cantidades de todos los pedidos del rango
        row_summary_lst.insert(0,a_product_name_lst[y]['name'])    #agrega el nombre al inicio de la lista
        row_summary_lst.insert(len(row_summary_lst),total)  # agrega el total al final de la lista
        summary_table.add_row(row_summary_lst)              # agrega filas a la tabla
        summary_table.align='l'
        #summary_table.align['Producto']='l'                 # alinea la a la izquierda la primera columna
        summary_table.align['Total']='r'                    # alinea a la derecha la ultima columna
    print summary_table                                     # imprime la tabla resumen
    with open ('consolidado.txt','w') as w:                 # escribe la tabla en un archivo txt
        w.write(str('ESTE ES EL CONSOLIDADO DE LOS SIGUIENTES PEDIDOS:'))
        w.write('\n')
        w.write(str(summary_table))
    return
