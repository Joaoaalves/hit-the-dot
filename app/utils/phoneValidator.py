import phonenumbers
from . import app

def is_a_valid_phone(number):
    phone = phonenumbers.parse(number, region='BR')
    return phonenumbers.is_valid_number(phone)

def international_phone(number):
    phone = phonenumbers.parse(number, region='BR')
    return phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

def national_phone(number):
    phone = phonenumbers.parse(number, region='BR')
    return phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.NATIONAL)

app.jinja_env.globals.update(national_phone=national_phone)
app.jinja_env.globals.update(international_phone=international_phone)