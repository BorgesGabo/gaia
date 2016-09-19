# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

import datetime

def sandbox():
    #this function is to experiment
    #rows=db().select(db.po.po_number)
    #for row in db(db.po.id>0).select():
     #   rtn = row
    
    
    #query = db.po.id==db.po_detail.po_id
    #query = db.po_detail.product_id==db.product.id
    #query &= db.po.po_number ==2424
    
    #query = db.po.id==db.po_detail.po_id
    #query &= db.po_detail.product_id==db.product.id
    #query &= db.product.id== db.po_detail.product_id
    #query &= db.po.po_number ==2424
    
    rows1=db.executesql('SELECT date, quantity FROM po, po_detail where po_detail.po_id=po.id',as_dict = True)
    
    # a query from 2 tables copied from http://stackoverflow.com/questions/11029538/sqlite-query-from-multiple-tables-using-sqlitedatabase
    
    #rows1=db.executesql('SELECT quantity, pres  FROM po_detail, product where po_detail.product_id=product.id',as_dict = True)
    count=len(rows1)
    #rows1=db(query).select(db.po_detail.product_id, db.product.pres)
    #count = db(rows1).count()
    msg = T("%s registers" % count )
    
    #rows2=db(query).select(db.po_detail.quantity)
    #rows3=db(query).select(db.po_detail.quantity*db.po_detail.po_id)
   # return dict(rows1=rows1,rows2=rows2,rows3=rows3)
    return dict(rows1=rows1, msg=msg)
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
    query &= db.po_detail.po_id==db.product.id
    

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
    #querysql= db.executesql('select * from results', as_dict=True)
    #querysql= db.executesql('select po_number,date,product_id,quantity,pres, customer_id from po,po_detail,product where () ', as_dict=True)
    querysqls=db(query).select(db.po_detail.product_id)
    #db.po.id==db.po_detail.po_id
    #query &= db.po_detail.po_id==db.product.id
    return dict(form=form, msg=msg, results=results, querysqls=querysqls) 

def results4():
    import datetime
    # this function is intented to provide a query from db.po. db.po_details and db.products filtered by dates
    #from : http://aprenda-web2py.blogspot.com.co
    query=db((db.po.date.year()==2016)&(db.po.date.month()==1)&(db.po.date.day()>1)).select(orderby='date')
    return dict(query=query)

def fechas():
    import datetime
    year=db((db.po.date.year()==datetime.date(session.fecha_hasta).year)&(db.po.date.month()==4)&(db.po.date.day()>1)).select(orderby='date')
    return dict(year=year)

def results3():
    from datetime import datetime
    #this query selects the columns from db.po_detail, db.po, and db.product that are related, creates a form based on dates types and once its submitted the user is redirected to fechas function
    form = SQLFORM.factory(
        Field('fecha_desde', type='datetime', requires=IS_NOT_EMPTY(), default=lambda:datetime.now()),
        Field('fecha_hasta', type='datetime', requires=IS_NOT_EMPTY()), default=lambda:datetime.now())
    if form.process().accepted:
        response.flash = 'form accepted'
        session.fecha_desde = form.vars.fecha_desde
        session.fecha_hasta = form.vars.fecha_hasta
        redirect(URL('fechas'))
    elif form.errors:
        response.flash = 'form has errors'
    query=db((db.po.id==db.po_detail.po_id)&(db.po_detail.po_id==db.product.id)).select(db.po.po_number,db.po.date, db.po_detail.product_id, db.po_detail.quantity, db.product.pres, db.po.customer_id)
    return dict(query=query, form=form,)

def results2():
    #this query selects the columns from db.po_detail and db.po that are related
    query=db((db.po.id==db.po_detail.po_id)).select(db.po.id,db.po.po_number,db.po.date,db.po_detail.id,db.po_detail.po_id,db.po_detail.product_id)
    return dict(query=query)

def results():
    query=db((db.po.po_number>2423)&(db.po.po_number<=2428)).select(db.po.id,db.po.po_number,db.po.date,db.po_detail.id,db.po_detail.po_id,db.po_detail.product_id)
    return dict(query=query)

def order():
    #This query selects all the po's from db.po ordered by reverse order
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
    #this function uploads and handles the form also uploads a query which select in reverse order all data in po_detail table
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
   form = SQLFORM(db.customer,buttons = [TAG.button('save',_type="submit"),TAG.button('next',_type="button",_onClick = "parent.location='%s' " % URL(form2))])

   if form.process().accepted:
       response.flash = 'form accepted'
   elif form.errors:
       response.flash = 'form has errors'
   else:
       response.flash = 'please fill out the form'
   return dict(form=form)

def form2():
   form = SQLFORM(db.po,buttons = [TAG.button('save',_type="submit"),TAG.button('next',_type="button",_onClick = "parent.location='%s' " % URL(form3))])
   if form.process().accepted:
       response.flash = 'form accepted'
   elif form.errors:
       response.flash = 'form has errors'
   else:
       response.flash = 'please fill out the form'
   return dict(form=form)

def form3():
   form = SQLFORM(db.po_detail)
   if form.process().accepted:
       response.flash = 'form accepted'
   elif form.errors:
       response.flash = 'form has errors'
   else:
       response.flash = 'please fill out the form'
   return dict(form=form)

  
def form4():
   form = SQLFORM(db.product)
   if form.process().accepted:
       response.flash = 'form accepted'
   elif form.errors:
       response.flash = 'form has errors'
   else:
       response.flash = 'please fill out the form'
   return dict(form=form)

def form5():
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
