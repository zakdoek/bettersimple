from datetime import datetime
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import simplejson

from reservation.models import *
from reservation.models import make_uuid
from clientservice.models import *
from message.models import *
from clientservice.forms import *
from reservation.forms import *

def edit_reservation_trip(request, client, trip):
    past_query = request.session.get('reservation_index_current_url', '')
    if request.method == "POST":
        trip_form = TripForm(request.POST, instance=trip)
        contact_form = ContactForm(request.POST, instance=trip.customer)
        pickup_address_form = AddressForm(request.POST, instance=trip.pickup_address, prefix="pickup")
        dropoff_address_form = AddressForm(request.POST, instance=trip.dropoff_address, prefix="dropoff")
        
        if trip_form.is_valid() and contact_form.is_valid() and pickup_address_form.is_valid() and dropoff_address_form.is_valid():
            contact = contact_form.save()
            pickup_address = pickup_address_form.save()
            dropoff_address = dropoff_address_form.save()
            trip = trip_form.save(commit=False)
            trip.customer = contact
            trip.pickup_address = pickup_address
            trip.dropoff_address = dropoff_address
            trip.uuid = make_uuid()
            trip.save()
            trip_form.save_m2m()
            Message.create_messages(reservation=trip, message_type=Message.RESERVATION_UPDATE_CONFIRM)
            request.session['show_confirmation'] = True
            request.session['confirmation_message'] =  ("The reservation for %s on %s was updated successfully!") % (contact.name, client.localize(trip.reservation_datetime).strftime("%m/%d/%Y"))
            return HttpResponseRedirect('/reservation/?'+past_query)
    else:
        trip_form = TripForm(instance=trip)
        contact_form = ContactForm(instance=trip.customer)
        pickup_address_form = AddressForm(instance=trip.pickup_address, prefix="pickup", client_id=request.user.profile.client.id)
        if trip.pickup_address.landmark_name != "" and ClientLandmark.objects.filter(name=trip.pickup_address.landmark_name, company=client):
            pickup_address_form.fields['landmarks'].initial = ClientLandmark.objects.filter(name=trip.pickup_address.landmark_name, company=client)[:1].get().id
        dropoff_address_form = AddressForm(instance=trip.dropoff_address, prefix="dropoff", client_id=request.user.profile.client.id)
        if trip.dropoff_address.landmark_name != "" and ClientLandmark.objects.filter(name=trip.dropoff_address.landmark_name, company=client):
            dropoff_address_form.fields['landmarks'].initial = ClientLandmark.objects.filter(name=trip.dropoff_address.landmark_name, company=client)[:1].get().id
    return render_to_response('reservation/trip/update.html', 
        {
            'industry_profile':client.industry_profile,
            'trip_form' : trip_form, 
            'trip':trip, 
            'contact_form':contact_form,
            'pickup_address_form':pickup_address_form,
            'dropoff_address_form':dropoff_address_form,
            'has_landmarks': client.landmarks.count() > 0,
            'client_landmarks': "["+"".join([l.address.json_string()+"," for l in client.landmarks.all()]).rstrip(',') + "]",
            'return_url': '/reservation/?'+past_query,
            'past_query': past_query
        },
        context_instance=RequestContext(request))
        
def edit_reservation_appointment(request, client, reservation):
    past_query = request.session.get('reservation_index_current_url', '')
    if request.method == "POST":
        reservation_form = ReservationForm(request.POST, instance=reservation)
        contact_form = ContactForm(request.POST, instance=reservation.customer)
        
        if reservation_form.is_valid() and contact_form.is_valid():
            contact = contact_form.save()
            reservation = reservation_form.save(commit=False)
            reservation.customer = contact
            reservation.uuid = make_uuid()
            reservation.save()
            reservation_form.save_m2m()
            Message.create_messages(reservation=reservation, message_type=Message.RESERVATION_UPDATE_CONFIRM)
            request.session['show_confirmation'] = True
            request.session['confirmation_message'] =  ("The reservation for %s on %s was updated successfully!") % (contact.name, client.localize(reservation.reservation_datetime).strftime("%m/%d/%Y"))
            return HttpResponseRedirect('/reservation/?' + past_query)
    else:
        reservation_form = ReservationForm(instance=reservation)
        contact_form = ContactForm(instance=reservation.customer)
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


def user_edit_trip(request, trip):
    success_message = None
    if request.method == "POST":
        trip_form = TripForm(request.POST, instance=trip)
        pickup_address_form = AddressForm(request.POST, instance=trip.pickup_address, prefix="pickup")
        dropoff_address_form = AddressForm(request.POST, instance=trip.dropoff_address, prefix="dropoff")
        
        if trip_form.is_valid() and pickup_address_form.is_valid() and dropoff_address_form.is_valid():
            pickup_address = pickup_address_form.save()
            dropoff_address = dropoff_address_form.save()
            trip = trip_form.save(commit=False)
            trip.pickup_address = pickup_address
            trip.dropoff_address = dropoff_address
            trip.uuid = make_uuid()
            trip.save()
            trip_form.save_m2m()
            Message.create_messages(reservation=trip, message_type=Message.RESERVATION_UPDATE_CONFIRM)
            success_message = "Your reservation has successfully been updated. You should receive with the details along with a link to edit the reservation again. You may close this window now."
    else:
        trip_form = TripForm(instance=trip)
        pickup_address_form = AddressForm(instance=trip.pickup_address, prefix="pickup", client_id=trip.company.id)
        if trip.pickup_address.landmark_name != "" and ClientLandmark.objects.filter(name=trip.pickup_address.landmark_name, company=client):
            pickup_address_form.fields['landmarks'].initial = ClientLandmark.objects.filter(name=trip.pickup_address.landmark_name, company=client)[:1].get().id
        dropoff_address_form = AddressForm(instance=trip.dropoff_address, prefix="dropoff", client_id=trip.company.id)
        if trip.dropoff_address.landmark_name != "" and ClientLandmark.objects.filter(name=trip.dropoff_address.landmark_name, company=client):
            dropoff_address_form.fields['landmarks'].initial = ClientLandmark.objects.filter(name=trip.dropoff_address.landmark_name, company=client)[:1].get().id
            
    return render_to_response('reservation/trip/update.html', 
        {
            'industry_profile':trip.company.industry_profile,
            'trip_form' : trip_form, 
            'trip':trip, 
            'pickup_address_form':pickup_address_form,
            'dropoff_address_form':dropoff_address_form,
            'user_edit': True,
            'success_message': success_message,
            'has_landmarks': (trip.company.landmarks.count() > 0),
            'client_landmarks': "["+"".join([l.address.json_string()+"," for l in trip.company.landmarks.all()]).rstrip(',') + "]"
        },
        context_instance=RequestContext(request))

def user_edit_appointment(request, reservation):
    success_message = None
    if request.method == "POST":
        reservation_form = ReservationForm(request.POST, instance=reservation)
        
        if reservation_form.is_valid():
            reservation = reservation_form.save(commit=False)
            reservation.uuid = make_uuid()
            reservation.save()
            reservation_form.save_m2m()
            Message.create_messages(reservation=reservation, message_type=Message.RESERVATION_UPDATE_CONFIRM)
            success_message = "Your reservation has successfully been updated. You should receive with the details along with a link to edit the reservation again. You may close this window now."
    else:
        reservation_form = ReservationForm(instance=reservation)
            
    return render_to_response('reservation/appointment/update.html', 
        {
            'industry_profile':reservation.company.industry_profile,
            'reservation_form' : reservation_form, 
            'reservation':reservation, 
            'user_edit': True,
            'success_message': success_message,
        },
        context_instance=RequestContext(request))
