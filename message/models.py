
import pytz
from datetime import datetime, timedelta
from django.db import models

from reservation.models import Reservation
from clientservice.models import Client


class Message(models.Model):
    # constants for message types
    RESERVATION_CREATE_CONFIRM = 0
    RESERVATION_UPDATE_CONFIRM = 1
    RESERVATION_REMINDER = 2
    RESERVATION_DELETED = 3
    RESERVATION_COMPANY_REPORT = 4
    CLIENT_CREATE_CONFIRM = 5
    CLIENT_UPDATE_CONFIRM = 6
    CLIENT_MONTHLY_CHARGE = 7
    CLIENT_PAYMENT_CONFIRM = 8
    RESERVATION_REMINDER_TEXT = 9

    # constants for message status
    UNSENT = 0
    PENDING = 1
    SENT = 2
    ERROR = 3
    
    reservation = models.ForeignKey(Reservation, null=True, blank=True)
    status = models.IntegerField(default=UNSENT)
    message_type = models.IntegerField()
    send_datetime = models.DateTimeField(default=datetime.now(pytz.utc))
    client = models.ForeignKey(Client, null=True, blank=True)
    monthly_charge = models.ForeignKey('charge.MonthlyCharge', null=True, blank=True)
    
    def __unicode__(self):
        if self.reservation:
            return "Id: %s Reservation Id: %s Status: %s" % (self.id, self.reservation.id, self.status)
        if self.client:
            return "Id: %s Client Id: %s Status: %s" % (self.id, self.client.id, self.status)
        if self.monthly_charge:
            return "Id: %s Monthly Charge Id: %s Status: %s" % (self.id, self.monthly_charge.id, self.status)
        return "Id: %s Status: %s" % (self.id, self.status)
        
    @staticmethod
    def create_client_message(client, message_type=CLIENT_CREATE_CONFIRM):
        if client == None:
            raise Exception("client is None")
        
        msg = Message()
        msg.status = Message.UNSENT
        msg.message_type = message_type
        msg.send_datetime = datetime.utcnow().replace(tzinfo=pytz.utc)
        msg.client = client
        msg.save()
        
        return msg
        
    @staticmethod
    def create_monthly_charge(charge):
        if charge == None:
            raise Exception("charge is None")
        
        msg = Message()
        msg.status = Message.UNSENT
        msg.message_type = Message.CLIENT_MONTHLY_CHARGE
        msg.send_datetime = datetime.utcnow().replace(tzinfo=pytz.utc)
        msg.monthly_charge = charge
        msg.save()
        
        return msg
        
    @staticmethod
    def create_payment_confirm(charge):
        if charge == None:
            raise Exception("charge is None")
        
        msg = Message()
        msg.status = Message.UNSENT
        msg.message_type = Message.CLIENT_PAYMENT_CONFIRM
        msg.send_datetime = datetime.utcnow().replace(tzinfo=pytz.utc)
        msg.monthly_charge = charge
        msg.save()
        
        return msg
    
    @staticmethod
    def create_reservation_message(reservation, message_type):
        if reservation == None:
            raise Exception("reservation is None")
        # delete any pre-existing messages for this reservation that are unsent
        [message.delete() for message in Message.objects.filter(reservation_id = reservation.id, status=Message.UNSENT)]
        
        confirm_msg = Message()
        confirm_msg.status = Message.UNSENT
        confirm_msg.message_type = message_type
        # send the confirmation message as soon as possible.
        confirm_msg.send_datetime = datetime.utcnow().replace(tzinfo=pytz.utc)
        confirm_msg.reservation = reservation
        confirm_msg.save()
        
        return confirm_msg


    @staticmethod
    def create_messages(reservation, message_type=RESERVATION_CREATE_CONFIRM):
        if reservation == None:
            raise Exception("reservation is None")
        # delete any pre-existing messages for this reservation that are unsent
        [message.delete() for message in Message.objects.filter(reservation_id = reservation.id, status=Message.UNSENT)]
        
        confirm_msg = Message.create_reservation_message(reservation, message_type)
        
        reminder_msg = Message()
        reminder_msg.status = Message.UNSENT
        reminder_msg.message_type = Message.RESERVATION_REMINDER
        # send out the reminder email a day before.
        reminder_msg.send_datetime = reservation.reservation_datetime - timedelta(days=1)
        reminder_msg.reservation = reservation
        reminder_msg.save()
        if reservation.send_reminder_text:
            text_reminder = Message()
            text_reminder.status = Message.UNSENT
            text_reminder.message_type = Message.RESERVATION_REMINDER_TEXT
            # send out the reminder email a day before.
            text_reminder.send_datetime = reservation.reservation_datetime - timedelta(days=1)
            text_reminder.reservation = reservation
            text_reminder.save()
        
        return [confirm_msg, reminder_msg]
    
