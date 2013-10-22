from django.conf import settings
import string
# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient



def send_text(to, message):
    ### Sends a text message to the given phone number with the given message via Twilio
    client = TwilioRestClient(account=settings.TWILIO_ACCOUNT_SID,
                              token=settings.TWILIO_AUTH_TOKEN)

    
    message = client.sms.messages.create(to=parse_number(to), from_=settings.TWILIO_FROM_NUMBER,
                                         body=message)

def parse_number(number):
    # Remove all the non-number characters
    return "+1"+number.translate(None, '() -.')