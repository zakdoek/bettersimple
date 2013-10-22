from datetime import datetime
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import simplejson

from reservation.models import *
from clientservice.models import *
from message.models import *
from clientservice.forms import *
from reservation.forms import *


def create_reservation_trip(request):
    trip = Trip()
    past_query = request.session.get('reservation_index_current_url', '')
    client = request.user.profile.client
    if request.method == "POST":
        trip_form = TripForm(request.POST)
        contact_form = ContactForm(request.POST)
        pickup_address_form = AddressForm(request.POST, prefix="pickup")
        dropoff_address_form = AddressForm(request.POST, prefix="dropoff")
        
        if trip_form.is_valid() and contact_form.is_valid() and pickup_address_form.is_valid() and dropoff_address_form.is_valid():
            contact = contact_form.save()
            pickup_address = pickup_address_form.save()
            dropoff_address = dropoff_address_form.save()
            trip = trip_form.save(commit=False)
            trip.customer = contact
            trip.pickup_address = pickup_address
            trip.dropoff_address = dropoff_address
            trip.company = client
            trip.customer_created = False
            try:
                # try to clean it again. If the reservation is made for 24 hours in advance it will raise an error.
                trip.clean()
                trip.save()
                trip_form.save_m2m()
                Message.create_messages(reservation=trip, message_type=Message.RESERVATION_CREATE_CONFIRM)
                request.session['show_confirmation'] = True
                request.session['confirmation_message'] = ("The reservation for %s on %s was created successfully!") % (contact.name, client.localize(trip.reservation_datetime).strftime("%m/%d/%Y"))
                return HttpResponseRedirect('/reservation/?'+past_query)
            except ValidationError as e:
                trip_form._errors["reservation_datetime"] = trip_form.error_class([e.messages[0]])
    else:
        trip_form = TripForm(instance=trip)
        contact_form = ContactForm(instance=Contact())
        pickup_address_form = AddressForm(instance=Address(), prefix="pickup", client_id=request.user.profile.client.id)
        dropoff_address_form = AddressForm(instance=Address(), prefix="dropoff", client_id=request.user.profile.client.id)
    return render_to_response('reservation/trip/update.html', 
        {
            'industry_profile':client.industry_profile,
            'trip_form' : trip_form, 
            'trip':trip, 
            'contact_form':contact_form,
            'pickup_address_form':pickup_address_form,
            'dropoff_address_form':dropoff_address_form,
            'has_landmarks': (client.landmarks.count() > 0),
            'client_landmarks': "["+"".join([l.address.json_string()+"," for l in client.landmarks.all()]).rstrip(',') + "]",
            'return_url': '/reservation/?'+past_query,
            'past_query': past_query
        },
        context_instance=RequestContext(request))

def create_reservation_appointment(request):
    reservation = Reservation()
    past_query = request.session.get('reservation_index_current_url', '')
    client = request.user.profile.client
    if request.method == "POST":
        reservation_form = ReservationForm(request.POST)
        contact_form = ContactForm(request.POST)
        
        if reservation_form.is_valid() and contact_form.is_valid():
            contact = contact_form.save()
            reservation = reservation_form.save(commit=False)
            reservation.customer = contact
            reservation.company = client
            reservation.customer_created = False
            try:
                reservation.clean()
                reservation.save()
                reservation_form.save_m2m()
                Message.create_messages(reservation=reservation, message_type=Message.RESERVATION_CREATE_CONFIRM)
                request.session['show_confirmation'] = True
                request.session['confirmation_message'] = ("The reservation for %s on %s was created successfully!") % (contact.name, client.localize(reservation.reservation_datetime).strftime("%m/%d/%Y"))
                return HttpResponseRedirect('/reservation/?'+past_query)
            except ValidationError as e:
                reservation_form._errors["reservation_datetime"] = reservation_form.error_class([e.messages[0]])
    else:
        reservation_form = ReservationForm(instance=reservation)
        contact_form = ContactForm(instance=Contact())
    return render_to_response('reservation/appointment/update.html', 
        {
            'industry_profile':client.industry_profile,
            'reservation_form' : reservation_form, 
            'reservation':reservation, 
            'contact_form':contact_form,
            'return_url': '/reservation/?'+past_query,
            'past_query': past_query
        },
        context_instance=RequestContext(request))
        
def user_create_reservation_trip(request, client):   
    trip = Trip()
    if request.method == "POST":
        trip_form = TripForm(request.POST)
        contact_form = ContactForm(request.POST)
        pickup_address_form = AddressForm(request.POST, prefix="pickup")
        dropoff_address_form = AddressForm(request.POST, prefix="dropoff")
        
        if trip_form.is_valid() and contact_form.is_valid() and pickup_address_form.is_valid() and dropoff_address_form.is_valid():
            contact = contact_form.save()
            pickup_address = pickup_address_form.save()
            dropoff_address = dropoff_address_form.save()
            trip = trip_form.save(commit=False)
            trip.customer = contact
            trip.pickup_address = pickup_address
            trip.dropoff_address = dropoff_address
            trip.company = client
            trip.customer_created = True
            try:
                trip.clean()
                trip.save()
                trip_form.save_m2m()
                Message.create_messages(reservation=trip, message_type=Message.RESERVATION_CREATE_CONFIRM)
                return HttpResponse(simplejson.dumps({'created':True}), mimetype='application/javascript')
            except ValidationError as e:
                trip_form._errors["reservation_datetime"] = trip_form.error_class([e.messages[0]])
        return HttpResponse(simplejson.dumps(
            {
                'use_special_instructions':client.industry_profile.use_special_instructions,
                'use_passengers':client.industry_profile.use_passengers,
                'created':False,
                'reservation_form':trip_form.errors, # use reservation_form for the name so the errors on the client side are handled correctly.
                'pickup_address_form':pickup_address_form.errors,
                'dropoff_address_form':dropoff_address_form.errors,
                'contact_form':contact_form.errors,
                'use_text_message_reminders' : client.industry_profile.use_text_message_reminders,
            }), mimetype='application/javascript')
    else:
        trip_form = TripForm(instance=trip)
        contact_form = ContactForm(instance=Contact())
        pickup_address_form = AddressForm(instance=Address(), prefix="pickup")
        dropoff_address_form = AddressForm(instance=Address(), prefix="dropoff")
    return render_to_response('reservation/trip/create.html', 
        {
            'use_special_instructions':client.industry_profile.use_special_instructions,
            'use_passengers':client.industry_profile.use_passengers,
            'trip_form' : trip_form, 
            'trip':trip, 
            'pickup_address_form':pickup_address_form,
            'dropoff_address_form':dropoff_address_form,
            'has_landmarks': (client.landmarks.count() > 0),
            'client_landmarks': "["+"".join([l.address.json_string()+"," for l in client.landmarks.all()]).rstrip(',') + "]",
            'contact_form':contact_form,
            'use_text_message_reminders' : client.industry_profile.use_text_message_reminders,
        },
        context_instance=RequestContext(request))

def user_create_reservation_appointment(request, client):   
    reservation = Reservation()
    if request.method == "POST":
        reservation_form = ReservationForm(request.POST)
        contact_form = ContactForm(request.POST)
        
        if reservation_form.is_valid() and contact_form.is_valid():
            contact = contact_form.save()
            reservation = reservation_form.save(commit=False)
            reservation.customer = contact
            reservation.company = client
            reservation.customer_created = True
            try:
                reservation.clean()
                reservation.save()
                reservation_form.save_m2m()
                Message.create_messages(reservation=reservation, message_type=Message.RESERVATION_CREATE_CONFIRM)
                return HttpResponse(simplejson.dumps({'created':True}), mimetype='application/javascript')
            except ValidationError as e:
                reservation_form._errors["reservation_datetime"] = reservation_form.error_class([e.messages[0]])
        return HttpResponse(simplejson.dumps(
            {
                'use_special_instructions':client.industry_profile.use_special_instructions,
                'use_passengers':client.industry_profile.use_passengers,
                'created':False,
                'reservation_form':reservation_form.errors,
                'pickup_address_form':'',
                'dropoff_address_form':'',
                'contact_form':contact_form.errors,
                'use_text_message_reminders' : client.industry_profile.use_text_message_reminders,
            }), mimetype='application/javascript')
    else:
        reservation_form = ReservationForm(instance=reservation)
        contact_form = ContactForm(instance=Contact())
    return render_to_response('reservation/appointment/create.html', 
        {
            'use_special_instructions':client.industry_profile.use_special_instructions,
            'use_passengers':client.industry_profile.use_passengers,
            'reservation_form' : reservation_form, 
            'reservation':reservation, 
            'contact_form':contact_form,
            'use_text_message_reminders' : client.industry_profile.use_text_message_reminders,
        },
        context_instance=RequestContext(request))
