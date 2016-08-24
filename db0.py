# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------------------------------------------------------------------------
#defining tables
#-----------------------------------------------------------------------------------------------------------------------------------------------------

db = DAL('sqlite://storage.sqlite')

db.define_table(
    'customer',
    Field('doc'),
    Field('full_name'),
    Field('user_mail'),
    Field('phone')
    )


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
