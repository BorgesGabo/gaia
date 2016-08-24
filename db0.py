# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#defining tables
#-----------------------------------------------------------------------------------------------------------------------------------------------------

db = DAL('sqlite://storage.sqlite')

db.define_table(
    'customer',
    Field('id'),
    Field('document'),
    Field('full_name'),
    Field('user_mail'),
    Field('phone')
    primarykey=['id'])

db.define_table(
    'po',
    Field('id'),
    Field('date', type='datetime'),
    Field('customer_id', db.customer),
    primarykey=['id'])

db.define_table(
    'product',
    Field('product_name'),
    Field('id'),
    Field('presentation'),
    Field('pres'),
    Field('unit'),
    Field('sku'),
    Field('categoria'),
    Field('status'),
    primarykey=['id'])

db.define_table(
    'po_detail',
    Field('po_id', db.po),
    Field('product_id', db.product),
    Field('po_product_name'),
    Field('quantity'),
    Field('po_sku'),
    )

#------------------------------------------------------------------------------------------------------------------------------------------------------
#customer table's constraints
#------------------------------------------------------------------------------------------------------------------------------------------------------

#using a regex expression validates the just numbers
db.customer.document.requires = [IS_NOT_IN_DB(db, db.customer.document),IS_MATCH('^[0-9]*$', error_message='Introduce a valid document just numbers')]

#using a regex expression validates words only
db.customer.full_name.requires = [IS_NOT_EMPTY(),IS_MATCH('^\w+( \w+)*$', error_message='Introduce a valid name just alphabets')]
db.customer.user_mail.requires = IS_EMAIL()

#using a regex expression validates the phone number format
# see more at... "http://stackoverflow.com/questions/16699007/regular-expression-to-match-standard-10-digit-phone-number"
db.customer.phone.requires = IS_MATCH('^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})?[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$',
         error_message='not a phone number. Introduce a valid number neither spaces nor dots')


#------------------------------------------------------------------------------------------------------------------------------------------------------
#product's table constrains
#------------------------------------------------------------------------------------------------------------------------------------------------------
#using regex expression to validate just one o more words 
db.product.product_name.requires = IS_MATCH('^\w+( \w+)*$', error_message='Introduce a valid name just alphabets')
db.product.id.requires=[IS_NOT_EMPTY(),IS_MATCH('^[0-9]*$', error_message='Introduce a valid document just numbers'), IS_NOT_IN_DB(db,db.product.id)]

db.product.presentation.requires = IS_NOT_EMPTY(error_message='copy here what is on product presentation in woocommerce' )
db.product.pres.requires = [IS_NOT_EMPTY(error_message='add a quantity' ),IS_MATCH('^[0-9]*$', error_message='Introduce a valid document just numbers')]
db.product.unit.requires =[ IS_IN_SET(['g','un'], error_message='must be g or un')]
db.product.sku.requires = [IS_NOT_IN_DB(db, db.product.sku),IS_MATCH('^[0-9]*$', error_message='Introduce a valid document just numbers')]
db.product.categoria.requires =[ IS_IN_SET(['aceites y aderezos','bebidas','condimentos y especias', 'frutas', 'frutos secos', 'harinas hojuelas y pastas', 'hortalizas', 'huevos','nueces y semillas','pa picar y endulzar','panaderia','proteina de  origen vegetal'], error_message='must be one of the existing categories')]
db.product.status.requires =[ IS_IN_SET(['disponible','descontinuado','agotado'], error_message='must be disponible, descontinuado o agotado')]


#------------------------------------------------------------------------------------------------------------------------------------------------------
#po's table constrains
#------------------------------------------------------------------------------------------------------------------------------------------------------

db.po.id.requires=[IS_NOT_EMPTY(),IS_MATCH('^[0-9]*$', error_message='Introduce a valid document just numbers'), IS_NOT_IN_DB(db,db.po.id)]
db.po.customer_id.requires=[IS_NOT_EMPTY(),IS_MATCH('^[0-9]*$', error_message='Introduce a valid document just numbers'),IS_IN_DB(db,db.customer.id)]
db.po.date.requires = IS_DATETIME(format=T('%Y-%m-%d %H:%M:%S'),error_message='must be YYYY-MM-DD HH:MM:SS!')



#-------------------------------------------------------------------------------------------------------------------------------------------------------
#po_details's table constrains
#-------------------------------------------------------------------------------------------------------------------------------------------------------

db.po_detail.po_id.requires= IS_IN_DB(db,db.po.id)
db.po_detail.product_id.requires=IS_IN_DB(db,'product.id', '%(product_name)s',zero=T('choose one'))
db.po_detail.po_product_name.requires=IS_IN_DB(db,db.product.product_name)
db.po_detail.quantity.requires=[IS_NOT_EMPTY(error_message='add a quantity'),IS_MATCH('^[0-9]*$', error_message='Introduce a valid quantity a number')]
db.po_detail.po_sku.requires=IS_IN_DB(db,db.product.sku)

#--------------------------------------------
#do not show the id field in the forms
#--------------------------------------------
db.customer.id.writable = db.customer.id.readable= True
db.product.id.writable = db.customer.id.readable= False
db.po.id.writable = db.po.id.readable= False
db.po_detail.po_sku.writable=db.po_detail.po_sku.readable=False
db.po_detail.po_product_name.writable=db.po_detail.po_product_name.readable=False
