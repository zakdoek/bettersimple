
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.localflavor.us.forms import USZipCodeField
from django.contrib.localflavor.us.us_states import US_STATES
from django import forms

from bettersimple.timezone import us_timezones

from clientservice.models import *
from reservation.models import ClientLandmark
from reservation.types import reservation_types, reservation_types_sorted
from bettersimple.custom_widgets import CheckboxSelectMultipleWithDetails

class PotentialClientForm(forms.ModelForm):
    class Meta:
        model = PotentialClient
        
class ClientForm(forms.ModelForm):
    zipcode = USZipCodeField(widget=forms.TextInput(attrs={'class': 'input-xlarge'}))
    class Meta:
        model = Client
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'client_phone': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'client_email': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'contact_name': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'contact_phone': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'contact_email': forms.TextInput(attrs={'class': 'input-xlarge'}),
            'address': forms.TextInput(attrs={'class':'input-xlarge'}),
            'city': forms.TextInput(attrs={'class':'input-xlarge'}),
            'state':  forms.Select(attrs={'class':'input-xlarge'},choices=US_STATES),
            'landmarks': CheckboxSelectMultipleWithDetails(attrs={'class':'input-xlarge unstyled'}),
            'timezone_name': forms.Select(attrs={'class':'input-xlarge'}, choices=[(tz, tz.replace('US/','')) for tz in us_timezones])
        }
        exclude = ('uuid', 'charge_profile', 'industry_profile',)
    
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        old_choices = self.fields['landmarks'].choices
        new_choices = []
        for i, (option_value, option_text) in enumerate(old_choices):
            new_choices.append((option_value, option_text, ClientLandmark.objects.filter(pk=option_value)[:1].get().html()))
            
        self.fields['landmarks'].choices = new_choices
    
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password1", "password2")

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class IndustryProfileForm(forms.ModelForm):
    class Meta:
        model = IndustryProfile
        widgets = {
            'reservation_type' : forms.Select(attrs={'class':'input-xlarge'}, choices=reservation_types_sorted),
        }
