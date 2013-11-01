import uuid
from datetime import datetime, timedelta

import pytz
from django.db import models
from django.core import validators

from common.custom_validators import *
from clientservice.models import Client


def make_uuid():
    return str(uuid.uuid4())
    
def escape(value):
    return value.replace(u'"', u'\\"')
    
def round_to_base(x, base=5, max_val=None):
    if max_val:
        return_val = int(base * round(float(x)/base))
        return return_val if return_val <= max_val else return_val - base
    return int(base * round(float(x)/base))
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=13, validators=[validate_phone_number])
    email = models.EmailField(max_length=254)
    
    def __unicode__(self):
        return self.email

class Address(models.Model):
    landmark_name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, validators=[validate_address])
    city = models.CharField(max_length=255, validators=[validate_city])
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)
    class Meta:
        verbose_name_plural = "addresses"
    
    def __unicode__(self):
        return "%s\t%s, %s  %s" % (self.address, self.city, self.state, self.zipcode)
    
    def address_string(self):
        return "%s\n%s\n%s, %s  %s" % (self.landmark_name, self.address, self.city, self.state, self.zipcode)
    
        
    def json_string(self):
        return '{"landmark_name":"%s","address":"%s","city":"%s","state":"%s","zipcode":"%s"}' % (escape(self.landmark_name), escape(self.address), escape(self.city), escape(self.state), escape(self.zipcode))
    
    def uses_landmark(self):
        return (self.landmark_name != "")
        
    def contains(self, search_term):
        search_term = search_term.lower()
        return (self.landmark_name.lower().find(search_term) > -1 or self.address.lower().find(search_term.lower()) > -1 or self.city.lower().find(search_term.lower()) > -1 or self.zipcode.lower().find(search_term.lower()) > -1)

class ClientLandmark(models.Model):
    name = models.CharField(max_length=255, validators=[validate_landmark])
    address = models.OneToOneField(Address)
    company = models.ForeignKey(Client)
    
    def __unicode__(self):
        return self.name
    
    def select_option_string(self):
        return '<option value="%s">%s</option>' % (self.id, self.name)
    
    
    def html(self):
        return '''
<address>
<strong>%s</strong><br>
%s<br>
%s, %s  %s
</address>
''' % (self.name, self.address.address, self.address.city, self.address.state, self.address.zipcode)

class ActiveReservationManager(models.Manager):
    def get_query_set(self):
        return super(ActiveReservationManager, self).get_query_set().filter(deleted=False)

class Reservation(models.Model):
    reservation_datetime = models.DateTimeField(default=(datetime.utcnow().replace(tzinfo=pytz.utc, minute=round_to_base(datetime.utcnow().minute, base=5, max_val=59)) + timedelta(days=1)))
    customer = models.ForeignKey(Contact)
    uuid = models.CharField(max_length=36, primary_key=False, default=make_uuid, editable=True)
    last_modified = models.DateTimeField(auto_now=True,auto_now_add=False)
    company = models.ForeignKey(Client)
    passengers = models.IntegerField(
        default=1, 
        validators=[validators.MinValueValidator(1), validators.MaxValueValidator(25)],
        error_messages={'min_value': ('Enter a value greater than 0.'), 'max_value': ('Enter a value less than 26')},
    )
    customer_created = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)
    special_instructions = models.TextField(default="", blank=True)
    send_reminder_text = models.BooleanField(default=False)
    
    # managers
    objects = models.Manager()
    active = ActiveReservationManager()
    
    def editable(self):
        return (not self.deleted) and self.company.local_now().replace(hour=0, minute=0, second=0, microsecond=0) <= self.company.localize(self.reservation_datetime)
    
    def clean(self):
        try:
            tomorrow = self.company.local_now() + timedelta(days=1)
            # Don't allow draft entries to have a pub_date.
            if self.reservation_datetime < tomorrow:
                raise ValidationError("The reservation must be made for a time that's at least 24 hours from now.")
        except Client.DoesNotExist:
            pass
            
    def __unicode__(self):
        try:
            name = "Trip" if self.trip else "Appt"
        except Trip.DoesNotExist:
            name = "Appt"
        return "%s for %s at %s for %s%s" % (name, self.customer, self.company.localize(self.reservation_datetime), self.company, " - deleted" if self.deleted else "")
            
    def csv_string(self):
        return [self.company.localize(self.reservation_datetime).strftime("%m/%d/%Y %I:%M %p"), self.customer.name, self.customer.phone, self.customer.email, self.passengers, self.special_instructions,  self.company.localize(self.last_modified).strftime("%m/%d/%Y %I:%M %p")]
        
class Trip(Reservation):
    pickup_address = models.OneToOneField(Address, related_name="Trip_pickup_address")
    dropoff_datetime = models.DateTimeField(default=(datetime.utcnow().replace(tzinfo=pytz.utc, minute=round_to_base(datetime.utcnow().minute, base=5, max_val=59)) + timedelta(days=1)))
    dropoff_address = models.OneToOneField(Address, related_name="Trip_dropoff_address")
    # managers
    objects = models.Manager()
    active = ActiveReservationManager()
    
    def __unicode__(self):
        return "Trip for %s at %s for %s%s" % (self.customer, self.company.localize(self.reservation_datetime), self.company, " - deleted" if self.deleted else "")
    
    def csv_string(self):
        return [self.company.localize(self.reservation_datetime).strftime("%m/%d/%Y %I:%M %p"), self.customer.name, self.customer.phone, self.customer.email, self.pickup_address.landmark_name, self.pickup_address.address, self.pickup_address.city, self.pickup_address.state, self.pickup_address.zipcode, self.dropoff_address.landmark_name, self.dropoff_address.address, self.dropoff_address.city, self.dropoff_address.state, self.dropoff_address.zipcode, self.passengers, self.special_instructions, self.company.localize(self.last_modified).strftime("%m/%d/%Y %I:%M %p")]
    
