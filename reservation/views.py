import csv
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.template import RequestContext
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.utils import simplejson, timezone
import pytz

from reservation.models import Reservation, Address, Contact
from clientservice.models import Client
from reservation.forms import ReservationForm, ContactForm, AddressForm

#defines the number of reservations per page to display
reservation_per_page = 3

@login_required()
def index(request):
    # only get those reservations that are associated with the logged in user's company
    timezone.activate('America/Denver')
    
    search_terms = request.GET.get('search_terms')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    if search_terms == None:
        search_terms = ""
    if start_date_str == None:
        start_date_str = ""
    if end_date_str == None:
        end_date_str = ""
    
    reservation_list = get_reservations(company=request.user.profile.client, search_terms=search_terms, start_date_str=start_date_str, end_date_str=end_date_str)
    paginator = Paginator(reservation_list, reservation_per_page)
    page = request.GET.get('page')
    try:
        reservations = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        reservations = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        reservations = paginator.page(paginator.num_pages)
    now = datetime.now()
    return render_to_response('reservation/index.html', 
        {
            'has_reservations' : (len(reservations) > 0),
            'reservations': reservations, 
            'client': request.user.profile.client,
            'search_terms': search_terms,
            'start_date': start_date_str,
            'end_date': end_date_str
        },
        context_instance=RequestContext(request))

@login_required()
def detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    return render_to_response('reservation/detail.html', {'reservation': reservation},context_instance=RequestContext(request))

@login_required()
@csrf_protect
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if request.method == "POST":
        reservation_form = ReservationForm(request.POST, instance=reservation)
        contact_form = ContactForm(request.POST, instance=reservation.customer)
        pickup_address_form = AddressForm(request.POST, instance=reservation.pickup_address, prefix="pickup")
        dropoff_address_form = AddressForm(request.POST, instance=reservation.dropoff_address, prefix="dropoff")
        
        if reservation_form.is_valid() and contact_form.is_valid() and pickup_address_form.is_valid() and dropoff_address_form.is_valid():
            # Figure out what this does, if anything!
            if request.is_ajax():
                retValue = serialize('json', [reservation])
                return HttpResponse(simplejson.dumps({'test':retValue}), mimetype='application/javascript')
            else:
                contact = contact_form.save()
                pickup_address = pickup_address_form.save()
                dropoff_address = dropoff_address_form.save()
                reservation = reservation_form.save(commit=False)
                reservation.customer = contact
                reservation.pickup_address = pickup_address
                reservation.dropoff_address = dropoff_address
                reservation.company = Client.objects.get(pk=1)
                reservation.save()
                reservation_form.save_m2m()
                return HttpResponseRedirect('/reservation/')
    else:
        reservation_form = ReservationForm(instance=reservation)
        contact_form = ContactForm(instance=reservation.customer)
        pickup_address_form = AddressForm(instance=reservation.pickup_address, prefix="pickup")
        dropoff_address_form = AddressForm(instance=reservation.dropoff_address, prefix="dropoff")
    return render_to_response('reservation/update.html', 
        {
            'reservation_form' : reservation_form, 
            'reservation':reservation, 
            'contact_form':contact_form,
            'pickup_address_form':pickup_address_form,
            'dropoff_address_form':dropoff_address_form
        },
        context_instance=RequestContext(request))
        
@login_required()
@csrf_protect
def create_reservation(request):
    reservation = Reservation()
    if request.method == "POST":
        reservation_form = ReservationForm(request.POST)
        contact_form = ContactForm(request.POST)
        pickup_address_form = AddressForm(request.POST, prefix="pickup")
        dropoff_address_form = AddressForm(request.POST, prefix="dropoff")
        
        if reservation_form.is_valid() and contact_form.is_valid() and pickup_address_form.is_valid() and dropoff_address_form.is_valid():
            contact = contact_form.save()
            pickup_address = pickup_address_form.save()
            dropoff_address = dropoff_address_form.save()
            reservation = reservation_form.save(commit=False)
            reservation.customer = contact
            reservation.pickup_address = pickup_address
            reservation.dropoff_address = dropoff_address
            reservation.company = request.user.profile.client
            reservation.save()
            reservation_form.save_m2m()
            return HttpResponseRedirect('/reservation/')
    else:
        reservation_form = ReservationForm(instance=Reservation())
        contact_form = ContactForm(instance=Contact())
        pickup_address_form = AddressForm(instance=Address(), prefix="pickup")
        dropoff_address_form = AddressForm(instance=Address(), prefix="dropoff")
    return render_to_response('reservation/update.html', 
        {
            'reservation_form' : reservation_form, 
            'reservation':reservation, 
            'contact_form':contact_form,
            'pickup_address_form':pickup_address_form,
            'dropoff_address_form':dropoff_address_form
        },
        context_instance=RequestContext(request))
        

@login_required()
@csrf_protect
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    pickup_address = reservation.pickup_address
    dropoff_address = reservation.dropoff_address
    customer = reservation.customer
    reservation.delete()
    pickup_address.delete()
    dropoff_address.delete()
    customer.delete()
    
    if request.is_ajax():
        return HttpResponse(simplejson.dumps({'success':1}), mimetype='application/javascript')
    else:
        return HttpResponseRedirect('/reservation/')

@login_required()
def download_to_csv(request):
    reservations = get_reservations(company=request.user.profile.client, search_terms=request.GET.get('search_terms'), start_date_str=request.GET.get('start_date'), end_date_str=request.GET.get('end_date'))
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=somefilename.csv'

    writer = csv.writer(response)
    
    writer.writerow(['Customer Name', 'Customer Phone', 'Customer Email', 'Pickup Time', 'Pickup Landmark', 'Pickup Address', 'Pickup City', 'Pickup State', 'Pickup Zipcode', 'Dropoff Time', 'Dropoff Landmark', 'Dropoff Address', 'Dropoff City', 'Dropoff State', 'Dropoff Zipcode'])
    for reservation in reservations:
        writer.writerow(reservation.csv_string(pytz.UTC))

    return response
    
def get_reservations(company, search_terms='', start_date_str="", end_date_str=""):
    # do some parameter validation
    if search_terms == None:
        search_terms = ""
    if start_date_str == None or start_date_str == "":
        start_date_str = ""
        start_date = datetime(1900,1,1, tzinfo=pytz.utc)
    else:
        start_date = datetime.strptime(start_date_str, '%m/%d/%Y')
        
    if end_date_str == None or end_date_str == "":
        end_date_str = ""
        end_date = datetime(2900,1,1, tzinfo=pytz.utc)
    else:
        end_date = datetime.strptime(end_date_str, '%m/%d/%Y')
    # convert to lower case so it's case insensitive
    search_terms = search_terms.lower()
    reservation_list = [reservation for reservation in Reservation.objects.filter(company = company, pickup_datetime__range=[start_date, end_date]).order_by('pickup_datetime')
            if reservation.customer.name.lower().find(search_terms) > -1 or reservation.pickup_address.contains(search_terms) or reservation.dropoff_address.contains(search_terms)]
    return reservation_list
