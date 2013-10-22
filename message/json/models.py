
import pytz
from datetime import datetime, timedelta
from django.conf import settings

from reservation import types

from reservation.models import Reservation
from message.models import Message
from clientservice.models import Client
from charge.models import *

class ContractMessage():
    to_email = ""
    from_email = ""
    bcc_email = ""
    subject = ""
    body = ""
    message_id = 0
        
    @staticmethod
    def subject(msg_type, company_name):
        return {
            Message.RESERVATION_CREATE_CONFIRM: 'Your reservation with %s has been created.' % ( company_name ),
            Message.RESERVATION_UPDATE_CONFIRM : 'Your reservation with %s has been updated.' % ( company_name ),
            Message.RESERVATION_REMINDER : 'Reminder about your reservation with %s.' % ( company_name ),
            Message.RESERVATION_DELETED : 'Your reservation with %s has been deleted.' % ( company_name ),
            Message.RESERVATION_COMPANY_REPORT : '%s Reservation Report' % ( company_name ),
            Message.CLIENT_CREATE_CONFIRM: 'Your account on Better Simple has been created.',
            Message.CLIENT_UPDATE_CONFIRM: '%s details on Better Simple has been created.' % ( company_name ),
            Message.CLIENT_MONTHLY_CHARGE: 'Better Simple Monthly Bill',
            Message.CLIENT_PAYMENT_CONFIRM: 'Better Simple Payment Confirmation',
        }[msg_type]
    
    @staticmethod
    def action(msg_type):
        return {
            Message.RESERVATION_CREATE_CONFIRM: 'created',
            Message.RESERVATION_UPDATE_CONFIRM : 'updated',
            Message.RESERVATION_REMINDER : '',
            Message.RESERVATION_DELETED : 'deleted',
            Message.RESERVATION_COMPANY_REPORT : '',
            Message.CLIENT_CREATE_CONFIRM: 'created',
            Message.CLIENT_UPDATE_CONFIRM: 'updated',
            Message.CLIENT_MONTHLY_CHARGE: '',
            Message.CLIENT_PAYMENT_CONFIRM: '',
        }[msg_type]
    
    @staticmethod
    def get_datetime_count_dictionary(reservations):
        date_dict = {}
        # create a dictionary of the number of reservations per hour
        for hour in range(0,24):
            date_dict[hour] = len([reservation for reservation in reservations if reservation.company.localize(reservation.reservation_datetime).hour == hour])
        return date_dict
    
    def __unicode__(self):
        return "message id:" % (self.message_id)
        
        
    @staticmethod
    def create(message):
        if message == None:
            raise Exception("message is None")
        contract_message = ContractMessage()
        contract_message.message_id = message.id
        contract_message.from_email = settings.EMAIL_HOST_USER
        contract_message.bcc_email = "schillingt@better-simple.com" if settings.DEBUG else ""
        
        if message.message_type == Message.RESERVATION_COMPANY_REPORT:
            contract_message.to_email = "schillingt@better-simple.com" if settings.DEBUG else message.client.contact_email
            contract_message.subject = ContractMessage.subject(message.message_type, message.client.name)
            contract_message.body = ContractMessage.get_body_for_company_report(message.client)
        elif message.message_type == Message.CLIENT_CREATE_CONFIRM or message.message_type == Message.CLIENT_UPDATE_CONFIRM:
            contract_message.to_email = "schillingt@better-simple.com" if settings.DEBUG else message.client.contact_email
            contract_message.subject = ContractMessage.subject(message.message_type, message.client.name)
            contract_message.body = ContractMessage.get_body_for_client(message, message.client)
        elif message.message_type == Message.CLIENT_MONTHLY_CHARGE:
            contract_message.to_email = "schillingt@better-simple.com" if settings.DEBUG else message.monthly_charge.client.contact_email
            contract_message.subject = ContractMessage.subject(message.message_type, message.monthly_charge.client.name)
            contract_message.body = ContractMessage.get_body_for_monthly_charge(message, message.monthly_charge)
        elif message.message_type == Message.CLIENT_PAYMENT_CONFIRM:
            contract_message.to_email = "schillingt@better-simple.com" if settings.DEBUG else message.monthly_charge.client.contact_email
            contract_message.subject = ContractMessage.subject(message.message_type, message.monthly_charge.client.name)
            contract_message.body = ContractMessage.get_body_for_payment_confirm(message, message.monthly_charge)
        elif message.message_type == Message.RESERVATION_CREATE_CONFIRM or message.message_type == Message.RESERVATION_UPDATE_CONFIRM or message.message_type == Message.RESERVATION_REMINDER or message.message_type == Message.RESERVATION_DELETED:
            
            reservation = message.reservation
            contract_message.to_email = "schillingt@better-simple.com" if settings.DEBUG else reservation.customer.email
            contract_message.subject = ContractMessage.subject(message.message_type, reservation.company.name)
            contract_message.body = ContractMessage.get_body_for_reservation_message(message, reservation)            
        return contract_message
    
    @staticmethod
    def get_body_for_company_report(company):
        startdate_utc = datetime.today().replace(tzinfo=pytz.UTC) - timedelta(days=1)
        enddate_utc = startdate_utc + timedelta(days=2)
        
        startdate = company.local_now().replace(hour=0,minute=0, second=0, microsecond=0)
        enddate = startdate + timedelta(days=1)
        
        reservations = [reservation for reservation in Reservation.active.filter(company_id=company, reservation_datetime__range=[startdate_utc, enddate_utc])
            if( company.localize(reservation.reservation_datetime) >= startdate and 
                company.localize(reservation.reservation_datetime) < enddate
            )]
        
        header = 'There are %s reservations are scheduled for today (%s). See below for the time breakdown or log into <a href="http://www.better-simple.com/reservation/">Better Simple</a> to view them.<br>' % (
            len(reservations),
            company.local_now().date().strftime("%m/%d/%y")
        )
        date_dict = ContractMessage.get_datetime_count_dictionary(reservations)
        
        body = '''
<br><strong>Hourly Reservation Breakdown</strong><br>
12:00 AM - %s<br>
1:00 AM - %s<br>
2:00 AM - %s<br>
3:00 AM - %s<br>
4:00 AM - %s<br>
5:00 AM - %s<br>
6:00 AM - %s<br>
7:00 AM - %s<br>
8:00 AM - %s<br>
9:00 AM - %s<br>
10:00 AM - %s<br>
11:00 AM - %s<br>
12:00 PM - %s<br>
1:00 PM - %s<br>
2:00 PM - %s<br>
3:00 PM - %s<br>
4:00 PM - %s<br>
5:00 PM - %s<br>
6:00 PM - %s<br>
7:00 PM - %s<br>
8:00 PM - %s<br>
9:00 PM - %s<br>
10:00 PM - %s<br>
11:00 PM - %s<br>
''' % (
            date_dict[0],
            date_dict[1],
            date_dict[2],
            date_dict[3],
            date_dict[4],
            date_dict[5],
            date_dict[6],
            date_dict[7],
            date_dict[8],
            date_dict[9],
            date_dict[10],
            date_dict[11],
            date_dict[12],
            date_dict[13],
            date_dict[14],
            date_dict[15],
            date_dict[16],
            date_dict[17],
            date_dict[18],
            date_dict[19],
            date_dict[20],
            date_dict[21],
            date_dict[22],
            date_dict[23],
        )
        
        footer = '<br>To view or edit the details of any of these reservations, please login at <a href="http://www.better-simple.com/reservation/">Better Simple</a>.'
        return "%s%s%s" % (header, body, footer)
    
    @staticmethod
    def get_body_for_client(message, client):
        header = '''
Hello %s,<br>
The account for %s has been %s. The details are below:<br>''' % ( 
            client.contact_name, 
            client.name, 
            ContractMessage.action(message.message_type) 
        )
        
        body = '''
<br><strong>Company Details</strong><br>
Company Name: %s<br>
Customer Service Phone #: %s<br>
Customer Service Email: %s<br>
Technical Contact: %s<br>
Technical Phone #: %s<br>
Technical Email: %s<br>
<br><strong>Address Information</strong><br>
Address: %s<br>
%s, %s  %s<br>
Use %s<br>
Use Special Instructions: %s<br>
<br><strong>Selected Landmarks</strong><br>
%s
''' % (
            client.name,
            client.client_phone,
            client.client_email,
            client.contact_name,
            client.contact_phone,
            client.contact_email,
            client.address,
            client.city,
            client.state,
            client.zipcode,
            ("Passengers: " if client.industry_profile.reservation_type == types.TRIP else "Attendees: ") + ("Yes" if client.industry_profile.use_passengers else "No"),
            "Yes" if client.industry_profile.use_special_instructions else "No",
            ("".join([l.name+"<br>" for l in client.landmarks.all()]) if client.landmarks.all().count() > 0 else "No landmarks are selected<br>")
        )
        
        footer = '<br>To modify the details further, please log into <a href="http://www.better-simple.com/clients/update/">Better Simple</a>.'
        
        return "%s%s%s" % ( header, body, footer)
    
    @staticmethod
    def get_body_for_monthly_charge(message, charge):
        header = 'Your bill for the month of %s is $%s. The details of the bill can be seen below. To view/download the invoice or to pay the bill online, please log into <a href="http://www.better-simple.com/charge/">Better Simple</a>.<br>' % ( charge.charge_date.strftime("%B"), charge.amount_due() )
        body = '''<br><strong>
# of reservations this month: %s<br>
Charge per reservation: $%s<br>
Amount Discounted: $%s<br>
Amount Due: %s<br></strong>''' % (
            ReservationCharge.objects.filter(monthly_charge_id=charge).count(),
            charge.client.charge_profile.charge_per_reservation,
            charge.discount_amount,
            charge.amount_due()
        )
        footer = '<br><br>Thank you for being a customer. If you have any questions, please contact us via <a href="mailto:schillingt@better-simple.com">email</a> or call/text at 970.682.3174'
        return "%s%s%s" % ( header, body, footer )
    
    @staticmethod
    def get_body_for_payment_confirm(message, charge):
        header = 'Your bill for the month of %s has been paid. The details of the bill can be seen below. To view/download the invoice or to pay the bill online, please log into <a href="http://www.better-simple.com/charge/">Better Simple</a>.<br>' % ( charge.charge_date.strftime("%B") )
        body = '''<br><strong>
# of reservations this month: %s<br>
Charge per reservation: $%s<br>
Amount Discounted: $%s<br>
Amount Charged: $%s<br>
Card Charged: $%s<br></strong>''' % (
            ReservationCharge.objects.filter(monthly_charge_id=charge).count(),
            charge.client.charge_profile.charge_per_reservation,
            charge.discount_amount,
            charge.amount_due(),
            (("*"*12) + stripe.Customer.retrieve(charge.client.charge_profile.stripe_customer_id)["active_card"]["last4"])
        )
        footer = '<br><br>Thank you for being a customer. If you have any questions, please contact us via <a href="mailto:schillingt@better-simple.com">email</a> or call/text at 970.682.3174'
        return "%s%s%s" % ( header, body, footer )
        
        
    @staticmethod
    def get_body_for_reservation_message(message, reservation):
        if message.message_type == Message.RESERVATION_REMINDER:
            header = '''
Hello %s,<br>
This is a reminder that you have a reservation with %s. The details are below:<br>''' % ( 
                reservation.customer.name, 
                reservation.company.name
            )
        else:
            header = '''
Hello %s,<br>
Your reservation with %s has been %s. The details are below:<br>''' % ( 
                reservation.customer.name, 
                reservation.company.name, 
                ContractMessage.action(message.message_type) 
            )
        try:
            trip = reservation.trip
            address_info = '''
<br><strong>Pickup Information</strong><br>
Time: %s<br>
Address: %s %s<br>
%s, %s  %s<br>
<br><strong>Dropoff Information</strong><br>
Address: %s %s<br>
%s, %s  %s<br>
%s%s<br>
''' % (
                reservation.company.localize(reservation.reservation_datetime).strftime("%m/%d/%Y, %I:%M %p"), 
                trip.pickup_address.landmark_name, 
                trip.pickup_address.address, 
                trip.pickup_address.city, 
                trip.pickup_address.state, 
                trip.pickup_address.zipcode, 
                trip.dropoff_address.landmark_name, 
                trip.dropoff_address.address, 
                trip.dropoff_address.city, 
                trip.dropoff_address.state, 
                trip.dropoff_address.zipcode,
                "Passengers: %s<br>" % reservation.passengers if reservation.company.industry_profile.use_passengers else "",
                "Special Instructions: <br>%s<br>" % reservation.special_instructions if reservation.company.industry_profile.use_special_instructions else "",
            )
        except Trip.DoesNotExist:
            address_info = '''
<br><strong>Reservation Details</strong><br>
Time: %s<br>
%s%s<br> 
''' % (
                reservation.company.localize(reservation.reservation_datetime).strftime("%m/%d/%Y, %I:%M %p"), 
                "Attendees: %s<br>" % reservation.passengers if reservation.company.industry_profile.use_passengers else "",
                "Special Instructions: %s<br>" % reservation.special_instructions if reservation.company.industry_profile.use_special_instructions else "",
            )
        
        footer = '''
<br>To modify this reservation, you can either call at %s or modify it yourself at <a href="http://www.better-simple.com/reservation/update/%s/%s/">Better Simple</a>.''' % (
            reservation.company.contact_phone, 
            reservation.id, 
            reservation.uuid
        )
        return "%s%s%s" % ( header, address_info, footer)

def get_text_message_reminder(reservation):
    return '''You have a reservation with %s on %s. If you have any questions please see your confirmation email or call %s.''' % (
           reservation.company.name,
           reservation.company.localize(reservation.reservation_datetime).strftime("%m/%d/%Y, %I:%M %p"),
           reservation.company.contact_phone, 
       )