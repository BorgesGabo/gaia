# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import datetime
from prettytable import PrettyTable
from prettytable import  ALL

def w():
    return

def table():
    
    pt = PrettyTable(["City name", "Area", "Population", "Annual Rainfall"])
    pt.align["City name"] = "l" # Left align city names
    pt.padding_width = 1 # One space between column edges and contents (default)
    pt.add_row(["Adelaide",1295, 1158259, 600.5])
    pt.add_row(["Brisbane",5905, 1857594, 1146.4])
    pt.add_row(["Darwin", 112, 120900, 1714.7])
    pt.add_row(["Hobart", 1357, 205556, 619.5])
    pt.add_row(["Sydney", 2058, 4336374, 1214.8])
    pt.add_row(["Melbourne", 1566, 3806092, 646.9])
    pt.add_row(["Perth", 5386, 1554769, 869.4])
    lines = pt.get_string()
    with open ('la_tabla.txt','w') as w:
        w.write(str(pt))
    print pt
    return

def merger():
    #This functions consolidates all the filtered po's according to the total quatities per product
    
    #1. Performs the filter by dates -> results = type(DAL. query), form= type(DAL, form),  msg=type(DAL, string)
    #------------------------------------------
    #1.0 defines the initial and final dates
    date_initial_default = \
        datetime.datetime.strptime(request.vars.date_initial, "%Y-%m-%d %H:%M:%S") \
            if request.vars.date_inicial else None
    date_final_default = \
        datetime.datetime.strptime(request.vars.date_final, "%Y-%m-%d %H:%M:%S") \
            if request.vars.date_final else None
    
    #1.1 The search form created with .factory
    form = SQLFORM.factory(
                  
                  Field("date_initial", "datetime", default=date_initial_default),
                  Field("date_final", "datetime", default=date_final_default),
                  formstyle='divs',
                  submit_button="Search",
                  )

    #1.2 The base query to fetch all orders of db.po, db.po_details, db.product
    query = db.po.id==db.po_detail.po_id
    query &= db.po_detail.product_id==db.product.id

    # 1.3 testing if the form was accepted              
    if form.process().accepted:
        # gathering form submitted values
        
        date_initial = form.vars.date_initial
        date_final = form.vars.date_final
        
        # more dynamic conditions in to query
        if date_initial:
            query &= db.po.date >= date_initial
        if date_final:
            query &= db.po.date <= date_final
                    
    #1.4 counts the total the number of registers 
    count = db(query).count()
    
    #1.5 returns the query results 
    results = db(query).select(db.po.po_number,db.po.date,db.po_detail.product_id,db.po_detail.quantity,db.product.pres, db.po.customer_id, orderby='po_number')
    #1.6 prints a message with the number of results
    msg = T("%s registers" % count )
    
    #2. gets all the products contained within the orders in 1. = A
    A=db(query).select(db.product.id, groupby='product.name')
    #2.1 convert A to a list
    A_rows=A.as_list()
    #2.2 gets the list's length and print it
    count2 = len(A_rows)
    msg2 = T("%s registers" % count2 )
  
    #3. consolidates all the quantities per po for each product  = B
    
    #3.1 retrieves the first product.id from A 
    Ai=A_rows[0]['id']
    
    #3.2 lists all the po.id in the range of dates
    orders=db(query).select(db.po.id, orderby='po.po_number',groupby='po.po_number' ).as_list()

    #for i, val in enumerate(orders):
    for a in orders:
        i=a['id']

        #i=0
        Bj=orders[i]['id']
        query_B=query
        #3.4 get the total quantity for the product.id(Ai)
        query_B &= db.po_detail.product_id==Ai
        Bijs=db(query_B).select(db.product.pres *db.po_detail.quantity, groupby='product.name')

    #4. gets all the subtotals per product                       = C
    #5. gets all the customers contained within the orders in 1. = D
    
    return dict(results=results, msg=msg, form=form, A=A, msg2=msg2, Ai=Ai,Bijs=Bijs ,orders=orders, i=i)

def B():

    #las condiciones para el query ->DAL> query
    query = db.po.id==db.po_detail.po_id
    query &= db.po_detail.product_id==db.product.id
    query &= db.po.po_number<2428
    
    #query_name = query
    #query_name &= db.po.customer_id==db.customer.id
    
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
    print str('*')*30
    print str('a_list: all products id in query no repeated are:')
    print a_list
   
    b_list=[]
    c_list=[]
    d_list=[]
    addend_of_c_list=[]
    
    
    #obtiene el primer elemento de a_list -> DAL> query_ai
    for i in range(len(a_list)):
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
                    # get the D
                    #d_list.append(db(query_b).select(db.customer.full_name).as_list())
                    #print str('d_list is')
                    #print d_list
                    
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
        print str('c erased is:')
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
    print str('a_list is:')
    print a_list
    
    #****************** IMPRIME TABLA RESUMEN ****
    a_names_lst=db(query).select(db.product.name, groupby='product.name').as_list()  #obtiene lista de nombres productos no repetidos en rango
    field_names_lst=[str(x['po_number']) for x in d_list ] #crea una lista con todos los numeros del pedido dentro del rango
    field_names_lst.insert(0, "Producto")                   # agrega al inicio de la lista el titulo producto 
    field_names_lst.insert(len(field_names_lst),"Total")    # Adiciona al final de la lista el titulo total
    summary_table=PrettyTable(field_names_lst)              # crea la tabla resumen con los titulos de cada columna
    for y in range (0,len(a_list)):
        #print str('quantity is')
        begining_slice=y*n                                  #definicion del inicio del intervalo de corte de la lista
        end_slice=begining_slice+n                          #definicion del fin del intervalo de corte de la lista
        row_summary_lst=b_list[begining_slice:end_slice]    #Toma los totales entre el incio y fin del intervalo sin tocar el fin
        row_summary_lst.insert(0,a_names_lst[y]['name'])    #agrega el nombre al inicio de la lista
        row_summary_lst.insert(len(row_summary_lst),c_list[y])  #agrega el total al final de la lista
        summary_table.add_row(row_summary_lst)              # agrega filas a la tabla
        summary_table.align['Producto']='l'
        
        print row_summary_lst
        #print begining_slice
        #print end_slice
        #print b_list[y]
        #print str('y es:')
        #print y
    '''print n
    print len(b_list)
    print len(a_list)
    
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
    
    print str('the summary table is:')
    print summary_table
    return 



def iterate():
    #This function is to perform iteration tests on the db
    query = db.po.id==db.po_detail.po_id
    query &= db.po_detail.product_id==db.product.id
    query &= db.po.po_number<2430
    #total = db.po_detail.quantity* db.product.pres
    
    #creates a DAL query and stores as a dictionary
    #result=db(query).select(db.po.id, db.po.po_number, db.po.date ,db.po_detail.product_id,db.po_detail.quantity,db.product.pres,  db.po.customer_id, total).as_dict()
    
    #this is a raw query
    #result=db.executesql('SELECT po.po_number,po_detail.product_id,product.name,product.pres FROM po,po_detail,product WHERE po.id==po_detail.po_id and po_detail.product_id==product.id and po.po_number<2428;',as_dict=True)
    
    #result=db.executesql('SELECT product.name, po_detail.id from po_detail, product, po WHERE po.id==po_detail.po_id and po_detail.product_id==product.id and po.po_number<2428;' ,as_dict=True )

    #This query removes the duplicates from the pos
    #result=db.executesql('SELECT min(po_detail.product_id), product.name, product.id FROM po_detail, product, po WHERE product.id==po_detail.product_id and po_detail.po_id==po.id and po.po_number<2428 GROUP BY po_detail.product_id',as_dict=True)
    
    result=db(query).select(db.po.id, orderby='po.po_number',groupby='po.po_number' ).as_list()
    # get all the products in the orders not repeated
    A=db(query).select(db.product.id, groupby='product.name').as_list()
    #filter the orders as a list and count the results
    pedidos_lst=db(query).select(db.po.po_number, orderby='po.po_number',groupby='po.po_number' ).as_list()
    n=len(pedidos_lst)
    b=[]
    
    for pedido in pedidos_lst:
        j=pedido['po_number'] #get the po_number from the dictionary for each pedido
        print str('j is:')
        print j
        query_B=query  #assign the query to a new query_B whose po_number and product belongs to Ai element and Bj element
        query_B &= db.po.po_number==j 
        print query_B
        query_B &= db.product.id ==A[0]['id']
        print query_B
        Bij=db(query_B).select(db.product.pres*db.po_detail.quantity).as_list()
        if not Bij:
            Bij[pedido]=0
            print str('list is empty')
        #print Bij[0]
        #Bij=Bij[0]['_extra']['(product.pres*po_detail.quantity)']
        #Bij=Bij['_extra']
        print str('Bij is:')
        print Bij
        b.append(Bij)
        print str('b is:')
        print b
     
    print str('el numero de pedidos es:')
    print n
    
    pedidos=pedidos_lst[0]['po_number']
    A=db(query).select(db.product.id, groupby='product.name').as_list()
    print str('los pedidos son:')
    print pedidos
    print str('A is:')
    print A
    
    #b=[]
    #for a in A:
        #i=a['id'] #get the id number from dictionary
        #query_A=query #assign the main query to a new one
        #get the 'i' product of A and retrieve the columns: name and pres
        #query_A &= db.product.id==i 
        #print str('i is:')
        #print i
        #result4 = db(query_A).select(db.product.name, db.product.pres, db.po_detail.quantity, orderby='po.po_number',groupby='po.po_number').as_list()
        #print str('result4 is:')
        #print result4
        
        #print str('b is:')
        #print b
        #result5=int(result4[0]['product']['pres'])
        #print str('result5 is:')
        #print result5
        #b.append(result5)
        #print str('b afert append is:')
        #print b
       
        
    #c:\Python27\python.exe c:\web2py\web2py.py -S EssenciaAPI24/default/iterate -M
     
    
    #retrieves the third's dictonary element
    #result=result[0]
    #key=result['id']
    
    #gets the dict' length
    count= len(result)
    msg = T("%s registers" % count )
    return dict(result=result, msg=msg, j=j)
    #return dict(result=result, msg=msg, pedidos=pedidos, result4=result4, b=b, result5=result5, n=n)
    
def sandbox():
    # this function is to perform queries tests on the db
    key=19
    query = db.po.id==db.po_detail.po_id
    query &= db.po_detail.product_id==db.product.id
    query &= db.po.po_number<2424
    #query &= db.product.id==key
    total = db.po_detail.quantity* db.product.pres
    result=db(query).select(db.po.id, db.po.po_number, db.po.date ,db.po_detail.product_id,db.po_detail.quantity,db.product.pres, total, db.po.customer_id)
    #gets the first element
    #result=result[0]
    #gets the column desired
    #result=result['_extra']
    #gets the value 
    #result=result['(po_detail.quantity * product.pres)']
    count = db(query).count()
    msg = T("%s registers" % count )
    return dict(result=result, msg=msg, form=form)

def start():
    # this function creates a form with date types and query the db between the 2 dates
    # this function is an extract from http://brunorocha.org/python/web2py/search-form-with-web2py.html
    # default values to keep the form when submitted
    # if you do not want defaults set all below to None
    
    
    
    date_initial_default = \
        datetime.datetime.strptime(request.vars.date_initial, "%Y-%m-%d %H:%M:%S") \
            if request.vars.date_inicial else None
    date_final_default = \
        datetime.datetime.strptime(request.vars.date_final, "%Y-%m-%d %H:%M:%S") \
            if request.vars.date_final else None
    


    # The search form created with .factory
    form = SQLFORM.factory(
                  
                  Field("date_initial", "datetime", default=date_initial_default),
                  Field("date_final", "datetime", default=date_final_default),
                  formstyle='divs',
                  submit_button="Search",
                  )

    # The base query to fetch all orders of db.po, db.po_details, db.product
    query = db.po.id==db.po_detail.po_id
    query &= db.po_detail.product_id==db.product.id
    

    # testing if the form was accepted              
    if form.process().accepted:
        # gathering form submitted values
        
        date_initial = form.vars.date_initial
        date_final = form.vars.date_final
        

        # more dynamic conditions in to query
        
        if date_initial:
            query &= db.po.date >= date_initial
        if date_final:
            query &= db.po.date <= date_final
                    

    count = db(query).count()
    results = db(query).select(db.po.po_number,db.po.date,db.po_detail.product_id,db.po_detail.quantity,db.product.pres, db.po.customer_id, orderby='po_number')
    msg = T("%s registers" % count )
    return dict(form=form, msg=msg, results=results) 

def order():
    #this function uploads and handles the form from db.po's table also uploads a query which select in reverse order all data in db.po's table
    ordenes=db(db.po.id>0).select(orderby=~db.po.id)
    form=SQLFORM(db.po, buttons =[TAG.button('save', _type="submit"),TAG.button('update', _type="button", _onClick ="parent.location='%s'" %URL(order)), TAG.button('next',_type="button", _onClick=" parent.location='%s'" %URL(orderd))])
    if form.process().accepted:
        response.flash='order accepted'
    elif form.errors:
        response.flash= 'check the data inserted'
    else:
        response.flash= 'please fill out the form'
    return dict(ordenes=ordenes, form=form)

def orderd():
    #this function uploads and handles the form from db.po_detail's table also uploads a query which select in reverse order all data in db.po_detail table
    ordenes=db(db.po_detail.id>0).select(orderby=~db.po_detail.po_id)
    form=SQLFORM(db.po_detail, buttons = [TAG.button('save',_type="submit"),TAG.button('update',_type="button",_onClick = "parent.location='%s' " % URL(orderd))])
    if form.process().accepted:
       response.flash = 'form accepted'
    elif form.errors:
       response.flash = 'form has errors'
    else:
       response.flash = 'please fill out the form'
    return dict(ordenes=ordenes, form=form)

def form1():
    #This function creates a form from db.customer's table
   form = SQLFORM(db.customer,buttons = [TAG.button('save',_type="submit"),TAG.button('next',_type="button",_onClick = "parent.location='%s' " % URL(form2))])

   if form.process().accepted:
       response.flash = 'form accepted'
   elif form.errors:
       response.flash = 'form has errors'
   else:
       response.flash = 'please fill out the form'
   return dict(form=form)

def form2():
    #This function creates a form from db.po's table
   form = SQLFORM(db.po,buttons = [TAG.button('save',_type="submit"),TAG.button('next',_type="button",_onClick = "parent.location='%s' " % URL(form3))])
   if form.process().accepted:
       response.flash = 'form accepted'
   elif form.errors:
       response.flash = 'form has errors'
   else:
       response.flash = 'please fill out the form'
   return dict(form=form)

def form3():
    #This function creates a form db.po_detail's form
   form = SQLFORM(db.po_detail)
   if form.process().accepted:
       response.flash = 'form accepted'
   elif form.errors:
       response.flash = 'form has errors'
   else:
       response.flash = 'please fill out the form'
   return dict(form=form)

def form4():
    #This function creates a form from db.product's table
   form = SQLFORM(db.product)
   if form.process().accepted:
       response.flash = 'form accepted'
   elif form.errors:
       response.flash = 'form has errors'
   else:
       response.flash = 'please fill out the form'
   return dict(form=form)

def form5():
    #This function creates a grid form from db.product's table
    grid = SQLFORM.grid(db.po_detail, user_signature=False)
    return locals()

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
