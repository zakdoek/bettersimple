from django import forms
from django.contrib.localflavor.us.forms import USZipCodeField
from django.contrib.localflavor.us.us_states import US_STATES
import unicodecsv

from reservation import types
from reservation.models import *
from clientservice.models import *
from bettersimple.custom_widgets import SelectTimeWidget, ClassSplitDateTimeWidget


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        widgets = {
            'name': forms.TextInput(attrs={'class': 'bsbt input-xlarge'}),
            'phone': forms.TextInput(attrs={'class': 'bsbt input-xlarge'}),
            'email': forms.TextInput(attrs={'class': 'bsbt input-xlarge'}),
        }

class AddressForm(forms.ModelForm):
    landmarks = forms.ModelChoiceField(
        queryset=ClientLandmark.objects.all(), # this gets overridden in the init function
        widget=forms.Select(attrs={'class':'bsbt input-xlarge landmark-select'}),
        empty_label="None", 
        required=False,
    )
    zipcode = USZipCodeField(widget=forms.TextInput(attrs={'class': 'bsbt input-xlarge'}))
    
    class Meta:
        model = Address
        widgets = {
            'address': forms.TextInput(attrs={'class':'bsbt input-xlarge address-field'}),
            'city': forms.TextInput(attrs={'class':'bsbt input-xlarge address-field'}),
            'state':  forms.Select(attrs={'class':'bsbt input-xlarge'},choices=US_STATES),
        }
        exclude = ('landmark_name',)
        
    def __init__(self, *args, **kwargs):
        client_id = kwargs.pop('client_id', None)
        super(AddressForm, self).__init__(*args, **kwargs)
        if client_id:
            self.fields['landmarks'].queryset = Client.objects.filter(pk=client_id)[:1].get().landmarks
        
    def save(self, force_insert=False, force_update=False, commit=True):
        m = super(AddressForm, self).save(commit=False)
        # if a landmark was selected, then use the address of that landmark.
        if self.cleaned_data['landmarks'] != None:
            landmark = Landmark.objects.filter(name=self.cleaned_data['landmarks'].name)[0]
            m.landmark_name = landmark.name
            m.address = landmark.address.address
            m.city = landmark.address.city
            m.state = landmark.address.state
            m.zipcode = landmark.address.zipcode
        else:
            m.landmark_name = ""
            
        if commit:
            m.save()
        return m
        
class LandmarkAddressForm(forms.ModelForm):
    zipcode = USZipCodeField(widget=forms.TextInput(attrs={'class': 'input-xlarge'}))
    class Meta:
        model = Address
        widgets = {
            'landmark_name': forms.TextInput(attrs={'class':'input-xlarge'}),
            'address': forms.TextInput(attrs={'class':'input-xlarge'}),
            'city': forms.TextInput(attrs={'class':'input-xlarge'}),
            'state':  forms.Select(attrs={'class':'input-xlarge'},choices=US_STATES),
        }
        
    def __init__(self, *args, **kwargs):
        super(LandmarkAddressForm, self).__init__(*args, **kwargs)
        self.fields['landmark_name'].required = True
    
    # commented out due to each company having it's own. They can manage their data.    
    #def clean_landmark_name(self):
    #    name = self.cleaned_data['landmark_name']
    #    if ClientLandmark.objects.filter(name=name).count() > 0:
    #        raise forms.ValidationError('The name "%s", has already been used. Use a unique name please.' % (name))
    #    return name
        
class UploadForm(forms.Form):
    reservation_file  = forms.FileField(widget=forms.ClearableFileInput(attrs={'style': 'display:none;'}))
    
    def clean(self):
        super(UploadForm, self).clean()
        cleaned_data = self.cleaned_data
        if not self.files['reservation_file'].name.endswith('.csv'):
            raise ValidationError('The file is not of extension ".csv", please export your file to a comma separated value file and upload it.')
        return cleaned_data
    
    def create_reservations(self, files, client, reservation_type, uses_landmarks):
        reservation_file = files['reservation_file']
        #line_of_text = ""
        #for chunk in reservation_file.chunks():
        if reservation_file.name.endswith('.csv'):
            return self.parse_csv(reservation_file, client, reservation_type, uses_landmarks)
    
    def parse_csv(self, reservation_file, client, reservation_type, uses_landmarks):
        r = unicodecsv.reader(reservation_file, encoding='utf-8')
        first_row = True
        while 1:
            try:
                row = r.next()
                if first_row:
                    print "first row"
                    first_row = False
                else:
                    reservation_datetime = datetime.strptime(row[0], "%m/%d/%Y %I:%M %p")
                    contact = Contact()
                    contact.name = row[1]
                    contact.phone = row[2]
                    contact.email = row[3]
                    if reservation_type == types.TRIP and uses_landmarks:
                        print "trip1"
                        trip = Trip()
                        trip.reservation_datetime = reservation_datetime
                        trip.company = client
                        pickup_address = Address()
                        dropoff_address = Address()
                        pickup_address.landmark_name = row[4]
                        pickup_address.address = row[5]
                        pickup_address.city = row[6]
                        pickup_address.state = row[7]
                        pickup_address.zipcode = row[8]
                        dropoff_address.landmark_name = row[9]
                        dropoff_address.address = row[10]
                        dropoff_address.city = row[11]
                        dropoff_address.state = row[12]
                        dropoff_address.zipcode = row[13]
                        trip.passengers = int(row[14])
                        trip.special_instructions = row[15]
                        contact.save()
                        pickup_address.save()
                        dropoff_address.save()
                        trip.customer = contact
                        trip.pickup_address = pickup_address
                        trip.dropoff_address = dropoff_address
                        trip.save()
                    elif reservation_type == types.TRIP:
                        print "trip2"
                        trip = Trip()
                        trip.reservation_datetime = reservation_datetime
                        trip.company = client
                        pickup_address = Address()
                        dropoff_address = Address()
                        pickup_address.landmark_name = ""
                        pickup_address.address = row[4]
                        pickup_address.city = row[5]
                        pickup_address.state = row[6]
                        pickup_address.zipcode = row[7]
                        dropoff_address.landmark_name = "" 
                        dropoff_address.address = row[8]
                        dropoff_address.city = row[9]
                        dropoff_address.state = row[10]
                        dropoff_address.zipcode = row[11]
                        trip.passengers = int(row[12])
                        trip.special_instructions = row[13]
                        contact.save()
                        pickup_address.save()
                        dropoff_address.save()
                        trip.customer = contact
                        trip.pickup_address = pickup_address
                        trip.dropoff_address = dropoff_address
                        trip.save()
                    else:
                        print "reservation"
                        reservation = Reservation()
                        reservation.reservation_datetime = reservation_datetime
                        reservation.company = client
                        reservation.passengers = int(row[4])
                        reservation.special_instructions = row[5]
                        contact.save()
                        reservation.customer = contact
                        reservation.save()
                    
            except StopIteration:
                print "end of file"
                break
        

class ReservationForm(forms.ModelForm):    
    class Meta:
        model = Reservation
        fields = ('reservation_datetime','passengers', 'special_instructions', 'send_reminder_text',)
        widgets = {
            'reservation_datetime': ClassSplitDateTimeWidget(date_format='%m/%d/%Y', time_format='%I:%M %p', attrs={'date_class':'bsbt input-medium datepicker', 'date_style':'', 'time_class':'bsbt input-small', 'time_style':'width:auto;'}),
            'passengers': forms.Select(attrs={'class':'bsbt input-small'}, choices=[(x,x) for x in range(1,21)]),
            'special_instructions': forms.Textarea(attrs={'class':'bsbt input-xlarge'}),
            'send_reminder_text': forms.CheckboxInput(),
        }
        
    

class TripForm(forms.ModelForm):    
    class Meta:
        model = Trip
        fields = ('reservation_datetime', 'passengers', 'special_instructions', 'send_reminder_text',) #'dropoff_datetime',
        widgets = {
            'reservation_datetime': ClassSplitDateTimeWidget(date_format='%m/%d/%Y', time_format='%I:%M %p', attrs={'date_class':'bsbt input-medium datepicker', 'date_style':'', 'time_class':'bsbt input-small', 'time_style':'width:auto;'}),
            'dropoff_datetime': ClassSplitDateTimeWidget(date_format='%m/%d/%Y', time_format='%I:%M %p', attrs={'date_class':'bsbt input-medium datepicker', 'date_style':'', 'time_class':'bsbt input-small', 'time_style':'width:auto;'}),
            'passengers': forms.Select(attrs={'class':'bsbt input-mini'}, choices=[(x,x) for x in range(1,21)]),
            'special_instructions': forms.Textarea(attrs={'class':'bsbt input-xlarge'}),
            'send_reminder_text': forms.CheckboxInput(),
        }
            
    def clean(self):
        cleaned_data = super(TripForm, self).clean()
        #reservation_datetime = cleaned_data.get("reservation_datetime")
        #dropoff_datetime = cleaned_data.get("dropoff_datetime")

        #if dropoff_datetime < reservation_datetime:
        #    raise forms.ValidationError("The dropoff time can't be before the pickup time")

        # Always return the full collection of cleaned data.
        return cleaned_data
