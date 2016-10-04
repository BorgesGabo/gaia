# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import datetime

def iterate():
    #This function is to perform iteration tests on the db
    query = db.po.id==db.po_detail.po_id
    query &= db.po_detail.product_id==db.product.id
    query &= db.po.po_number<2428
    #total = db.po_detail.quantity* db.product.pres
    
    #creates a DAL query and stores as a dictionary
    #result=db(query).select(db.po.id, db.po.po_number, db.po.date ,db.po_detail.product_id,db.po_detail.quantity,db.product.pres,  db.po.customer_id, total).as_dict()
    
    #this is a raw query
    #result=db.executesql('SELECT po.po_number,po_detail.product_id,product.name,product.pres FROM po,po_detail,product WHERE po.id==po_detail.po_id and po_detail.product_id==product.id and po.po_number<2428;',as_dict=True)
    
    #result=db.executesql('SELECT product.name, po_detail.id from po_detail, product, po WHERE po.id==po_detail.po_id and po_detail.product_id==product.id and po.po_number<2428;' ,as_dict=True )
    
    #This query removes the duplicates from the pos
    #result=db.executesql('SELECT min(po_detail.product_id), product.name FROM po_detail, product WHERE product.id==po_detail.product_id GROUP BY po_detail.product_id',as_dict=True)
    
    #This query removes the duplicates from the pos
    #taken from http://stackoverflow.com/questions/25884095/how-can-i-delete-duplicates-in-sqlites
    result=db.executesql('SELECT min(po_detail.product_id), product.name FROM po_detail, product, po WHERE product.id==po_detail.product_id and po_detail.po_id==po.id and po.po_number<2428 GROUP BY po_detail.product_id',as_dict=True)
    
    #calculates the dict's length
    #result=len(result)
    
    #retrieves the third's dictonary element
    #result=result[0]
    
    #count = db(query).count()
    count= len(result)
    msg = T("%s registers" % count )
    return dict(result=result, msg=msg)
    
def sandbox():
    # this function is to perform queries tests on the db
    query = db.po.id==db.po_detail.po_id
    query &= db.po_detail.product_id==db.product.id
    total = db.po_detail.quantity* db.product.pres
    result=db(query).select(db.po.id, db.po.po_number, db.po.date ,db.po_detail.product_id,db.po_detail.quantity,db.product.pres, total, db.po.customer_id)
    count = db(query).count()
    msg = T("%s registers" % count )
    return dict(result=result, msg=msg)

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
