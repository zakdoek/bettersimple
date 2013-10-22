#
#  HAD TO MODIFY THE DECIMAL.PY FILE FOR PYTHON2.6 SO THAT IT CAN CONVERT FROM FLOAT TO DECIMAL.
#  THE SAME METHOD FROM 2.7 WAS USED, HOWEVER IF A NEW MACHINE IS USED IT WILL FAIL.
# added import math as _math and added the Decimal.from_float method from 2.7, converts to a string and then to a decimal. Don't trust completely.
import pytz

from datetime import datetime, timedelta
from django.db import models

from reservation.models import *
from clientservice.models import Client
from message.models import Message

class ClientChargeProfile(models.Model):
    free_reservations = models.IntegerField(default=0)
    charge_per_reservation = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    charge_per_month = models.DecimalField(max_digits=6, decimal_places=2, default=20.00)
    charge_per_message = models.DecimalField(max_digits=5, decimal_places=2, default=0.02)
    
    def __unicode__(self):
        return "Id: %s Charge/Month: %s Charge/Res: %s Charge/Msg: %s Stripe Id: %s" % (
            self.id,
            self.charge_per_month,
            self.charge_per_reservation,
            self.charge_per_message,
            self.stripe_customer_id
        )
        
class MonthlyCharge(models.Model):
    client = models.ForeignKey(Client)
    charge_date = models.DateField()
    charge_amount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)
    discount_amount = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    stripe_charge_id = models.CharField(max_length=255, blank=True)
    
    
    def due_date(self):
        return (self.charge_date + timedelta(month=1)).replace(day=1)
        
    def amount_due(self):
        return (self.charge_amount - self.discount_amount)
    
    def __unicode__(self):
        return "Id: %s Date: %s Client: %s Charge: %s Discount: %s Amount Due: %s Paid: %s" % (
            self.id, 
            self.charge_date,
            self.client.name, 
            self.charge_amount,
            self.discount_amount,
            self.amount_due(),
            self.paid
        )
    
    @staticmethod
    def create_for_month(client, date, save=True):
        if client == None:
            raise Exception("client is None")
        if date == None:
            raise Exception("date is None")
        monthly_charge = MonthlyCharge()
        monthly_charge.client = client
        monthly_charge.charge_date = date.replace(day=1)
        paid = False
        # Find the reservations for this client this month that haven't already been billed for.
        reservations = [reservation for reservation in Reservation.active.filter(company_id=client, reservation_datetime__month=date.month)
            if ReservationCharge.objects.filter(reservation_id=reservation).count() == 0]
        
        # Assign the charge per month to the charge amount.
        monthly_charge.charge_amount = client.charge_profile.charge_per_month
        
        text_messages = []
        # Assign the reservation charges
        # add any non-customer created reservations to the free reservation count. Clients don't get charged if they create them.
        for reservation in reservations:
            if not reservation.customer_created:
                client.charge_profile.free_reservations += 1
            text_messages = Message.objects.filter(message_type=Message.RESERVATION_REMINDER_TEXT, reservation=reservation)
        
        charge_per_reservation = client.charge_profile.charge_per_reservation
        free_left = client.charge_profile.free_reservations
        monthly_charge.charge_amount += len(reservations) * charge_per_reservation
        # If there are more free than reservations this past month, then discount is equal to charge_amount
        if free_left >= len(reservations):
            monthly_charge.discount_amount += monthly_charge.charge_amount
            client.charge_profile.free_reservations = free_left - len(reservations)
        else:
            monthly_charge.discount_amount += free_left * charge_per_reservation
            client.charge_profile.free_reservations = 0
        
        charge_per_message = client.charge_profile.charge_per_message
        monthly_charge.charge_amount += len(text_messages) * charge_per_message
        
        monthly_charge.paid = (monthly_charge.amount_due() == 0)
        if save:
            # if the amount due is 0, then it's already been paid.
            client.charge_profile.save()
            monthly_charge.save()
            # Be sure to create a reservation charge for all of the charges that were billed for.
            # This will allow us to keep track of which reservations were billed
            for reservation in reservations:
                reservation_charge = ReservationCharge()
                reservation_charge.reservation = reservation
                reservation_charge.monthly_charge = monthly_charge
                reservation_charge.save()
            for message in text_messages:
                message_charge = MessageCharge()
                message_charge.message = text_message
                message_charge.monthly_charge = monthly_charge
                message_charge.save()
        return monthly_charge

class ReservationCharge(models.Model):
    monthly_charge = models.ForeignKey(MonthlyCharge)
    reservation = models.ForeignKey(Reservation)
    
    def __unicode__(self):
        return "Id: %s Monthly Charge Id: %s Client: %s Reservation Id: %s" % (
            self.id,
            self.monthly_charge.id,
            self.monthly_charge.client.name,
            self.reservation.id
        ) 

class MessageCharge(models.Model):
    monthly_charge = models.ForeignKey(MonthlyCharge)
    message = models.ForeignKey(Message)
    
    def __unicode__(self):
        return "Id: %s Monthly Charge Id: %s Client: %s Message Id: %s" % (
            self.id,
            self.monthly_charge.id,
            self.monthly_charge.client.name,
            self.message.id
        ) 
