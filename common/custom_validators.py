import re

from django.core.exceptions import ValidationError

from common.timezone import us_timezones


# (XXX)XXX-XXXX
# XXX-XXX-XXXX
# XXXXXXXXXX
phone_re = re.compile('^(\(\d\d\d\)\d\d\d-\d\d\d\d)|(\d\d\d-\d\d\d-\d\d\d\d)|(\d\d\d\d\d\d\d\d\d\d)$')

def validate_phone_number(value):
    check_if_empty(value)
    match = phone_re.match(value)
    if not match:
        raise ValidationError(u'Please enter a phone number in one of the following formats: (XXX)XXX-XXXX, XXX-XXX-XXXX or XXXXXXXXXX.')
    
def validate_address(value):
    check_if_empty(value)
    
def validate_city(value):
    check_if_empty(value)

def validate_landmark(value):
    check_if_empty(value)
    
def check_if_empty(value):
    """determines if the value is empty"""
    if len(value.rstrip()) == 0:
        raise ValidationError(u'This field must be filled out.')
        
def validate_timezone_name(value):
    if not value in us_timezones:
        raise ValidationError(u'Please select a valid US timezone.')
