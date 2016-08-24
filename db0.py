#-----------------------------------------------------------------------------------------------------------------------------------------------------
#defining tables
#-----------------------------------------------------------------------------------------------------------------------------------------------------

db = DAL('sqlite://storage.sqlite')

db.define_table(
    'customer',
    Field('doc'),
    Field('full_name'),
    Field('user_mail'),
    Field('phone'),
    format='%(full_name)s')

db.define_table(
    'po',
    Field('po_number'),
    Field('date', type='datetime'),
    Field('customer', db.customer),
    format='%(po_number)s')




#------------------------------
#Customer's table constraints
#------------------------------

#using a regex expression validates the just numbers
db.customer.doc.requires = [IS_NOT_IN_DB(db, db.customer.doc),IS_MATCH('^[0-9]*$', error_message='Introduce a valid document just numbers')]

#using a regex expression validates words only
db.customer.full_name.requires = [IS_NOT_EMPTY(),IS_MATCH('^\w+( \w+)*$', error_message='Introduce a valid name just alphabets')]
db.customer.user_mail.requires = IS_EMAIL()

#using a regex expression validates the phone number format
# see more at... "http://stackoverflow.com/questions/16699007/regular-expression-to-match-standard-10-digit-phone-number"
db.customer.phone.requires = IS_MATCH('^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})?[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$',
         error_message='not a phone number. Introduce a valid number neither spaces nor dots')

#-----------------------------
#po's table constraints
#-----------------------------

db.po.po_number.requires=[IS_NOT_EMPTY(),IS_MATCH('^[0-9]*$', error_message='Introduce a valid document just numbers'), IS_NOT_IN_DB(db,db.po.po_number)]
db.po.date.requires = IS_DATETIME(format=T('%Y-%m-%d %H:%M:%S'),error_message='must be YYYY-MM-DD HH:MM:SS!')
