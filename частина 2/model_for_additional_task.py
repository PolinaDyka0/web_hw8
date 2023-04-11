from mongoengine import *

class Contactadd(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    phone_number = StringField(required=True)
    email_sent = BooleanField(default=False)
    sms_sent = BooleanField(default=False)
    preferred_method = StringField(choices=['email', 'sms'], default='email')
