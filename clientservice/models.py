import uuid
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import pytz
from reservation import types

from common.custom_validators import *

def make_uuid():
    return str(uuid.uuid4())

class IndustryProfile(models.Model):
    reservation_type = models.IntegerField(default=0)
    use_special_instructions = models.BooleanField(default=False)
    use_passengers = models.BooleanField(default=False)
    use_text_message_reminders = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s Use instructions: %s Use Passengers: %s" % (
            types.to_string(self.reservation_type), 
            self.use_special_instructions, 
            self.use_passengers
        )
    
class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255, validators=[validate_address])
    city = models.CharField(max_length=255, validators=[validate_city])
    state = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=10)
    client_phone = models.CharField(max_length=13, validators=[validate_phone_number])
    client_email = models.EmailField(max_length=254)
    contact_phone = models.CharField(max_length=13, validators=[validate_phone_number])
    contact_email = models.EmailField(max_length=254)
    contact_name = models.CharField(max_length=255)
    uuid = models.CharField(max_length=36, primary_key=False, default=make_uuid, editable=True)
    landmarks = models.ManyToManyField('reservation.ClientLandmark', blank=True)
    charge_profile = models.OneToOneField('charge.ClientChargeProfile')
    timezone_name = models.CharField(max_length=100, default='US/Mountain', validators=[validate_timezone_name])
    industry_profile = models.OneToOneField(IndustryProfile)
    
    def localize(self, value):
        return value.astimezone(pytz.timezone(self.timezone_name))
    
    def local_now(self):
        return self.localize(datetime.utcnow().replace(tzinfo=pytz.UTC))
        
    def __unicode__(self):
        return "%s - Industry: %s" % (
            self.name, 
            types.to_string(self.industry_profile.reservation_type)
        )
        
class ClientCode(models.Model):
    client = models.OneToOneField(Client, parent_link=False)
    code = models.TextField()
    head_code = models.TextField()
    link_code = models.TextField()
    last_modified = models.DateTimeField(auto_now=True,auto_now_add=False)
    
    def __unicode__(self):
        return "%s's code" % (self.client.name)
    
    def set_defaults(self):
        base_url = settings.STATIC_URL
        self.link_code = '''
<button id="better-simple-link" href="#"></button>'''
        self.head_code = '''
<script type='text/javascript' src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
<script type="text/javascript" src="%sjquery-ui-1.8.20.custom.min.js"></script>
<script type="text/javascript" src="%sbootstrap/js/bootstrap.min.js"></script>
<script type="text/javascript" src="%sclient/head.js"></script>
<script type="text/javascript" src="%sjson2.js"></script>
<script type='text/javascript'>
var id = %s;
var uuid = '%s';
!(function($){
    $(document).ready(function(){
        SetupEvents(id, uuid);      
    });
})(window.jQuery);
</script>
''' % ( base_url,base_url,base_url,base_url, self.client.id, self.client.uuid )
        # save the new code segments
        self.save()
        
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    client = models.ForeignKey(Client)

class PotentialClient(models.Model):
    email = models.EmailField(max_length=254)
    
    def __unicode__(self):
        return self.email
    
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
