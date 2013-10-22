
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.utils import simplejson
import json
import stripe

from clientservice.models import *
from charge.models import *
from message.models import *

@login_required()
def past_charge(request, year, month):
    client = request.user.profile.client
    past_charge = MonthlyCharge.objects.get(client_id=client, charge_date__month=month, charge_date__year=year)
    if not past_charge:
        return HttpResponseRedirect('/charge/billing/')
    
    reservation_count = ReservationCharge.objects.filter(monthly_charge_id=past_charge).count()
    
    return render_to_response('charge/past_charge.html',
    {
        'paid': past_charge.paid,
        'reservation_count': reservation_count,
        'past_charge': past_charge,
        'past_charges': [(c.charge_date.strftime("%b %Y"), c.charge_date.strftime("%Y %m")) for c in MonthlyCharge.objects.filter(client_id=client, paid=True).order_by('-charge_date')]
    },
    context_instance=RequestContext(request))

@login_required()
def billing(request):
    client = request.user.profile.client
    total_charge = 0
    pending_charges = []
    show_confirmation = get_session_value(request, "show_confirmation", True)
    confirmation_message = get_session_value(request, "confirmation_message", True)
    
    charges = MonthlyCharge.objects.filter(client_id=client, paid=False).order_by('charge_date')
    
    if request.method == "POST" and client.charge_profile.stripe_customer_id != "":
        for charge in charges:
            charge.paid = True
            Message.create_payment_confirm(charge)
            stripe_charge = stripe.Charge.create(
                amount = int(charge.amount_due()*100),
                currency="usd",
                customer=client.charge_profile.stripe_customer_id
            )
            charge.stripe_charge_id = stripe_charge.id
            charge.save()
        show_confirmation = True
        confirmation_message = "Your card has been charged successfully."
    else:
        for charge in charges:
            reservation_count = ReservationCharge.objects.filter(monthly_charge_id=charge).count()
            pending_charges.append((charge.charge_date, reservation_count, charge.amount_due()))
            total_charge += charge.amount_due()
    
    # fetch the last 4 of the client's card
    token = stripe.Customer.retrieve(client.charge_profile.stripe_customer_id)['active_card'] if client.charge_profile.stripe_customer_id != "" else None
    
    if token:
        card_number = ("*"*12) + token["last4"]
    else:
        card_number = ""
    return render_to_response('charge/billing.html',
    {
        'card_number': card_number,
        'pending_charges': pending_charges,
        'total_charge': total_charge,
        'show_confirmation': show_confirmation,
        'confirmation_message': confirmation_message,
        'past_charges': [(c.charge_date.strftime("%b %Y"), c.charge_date.strftime("%Y %m")) for c in MonthlyCharge.objects.filter(client_id=client, paid=True).order_by('-charge_date')]
    },
    context_instance=RequestContext(request))
    

@csrf_exempt
def process_monthly_charges(request,token):
    #if settings.CHARGE_TOKEN != token or request.method != "POST":
    #    raise Http404
    
    clients = Client.objects.all()
    # the billing month is the one previous to this.
    date = (datetime.utcnow().replace(tzinfo=pytz.UTC, day=1) - timedelta(days=2)).date()
    for client in clients:
        monthly_charge = MonthlyCharge.objects.filter(charge_date__month=date.month, client_id=client)[:1]
        if not monthly_charge:
            # create the monthly charge
            charge = MonthlyCharge.create_for_month(client, date)
            # send out customer email
            monthly_charge = Message.create_monthly_charge(charge)
            pass
            
    return HttpResponse(simplejson.dumps({'success':True}), mimetype='application/javascript')
    
@csrf_exempt
def stripe_webhook(request, token):
    #if settings.CHARGE_TOKEN != token or request.method != "POST":
    #    raise Http404
    
    try:
        event_json = json.loads(request.body)
    #    stripe_event = stripe.Event.retrieve(event_json['id'])
    #    if stripe_event.type == 'invoice.created':
    #        return handle_invoice_created(stripe_event)
    except ValueError:
        pass
    return HttpResponse(status=200)

def handle_invoice_created(invoice_created):
    # get the client
    #stripe_customer_id = invoice_created.data.object.customer
    #charge_profile = ClientChargeProfile.objects.filter(stripe_customer_id=stripe_customer_id)[:1]
    #client = Client.objects.filter(charge_profile_id=charge_profile)[:1]
    
    # the billing month is the one previous to this.
    #date = (datetime.utcnow().replace(tzinfo=pytz.UTC) - timedelta(month=1)).date()
    #monthly_charge = MonthlyCharge.objects.get(charge_date__month=date.month, client_id=client)
    #if not monthly_charge:
        # create the monthly charge
    #    charge = MonthlyCharge.create_for_month(client, date)
    #    monthly_charge = Message.create_monthly_charge(charge)
    
    # add the invoice item (monthly charge)
    if not invoice_created.data.object.paid:
        stripe_invoice_item = stripe.InvoiceItem.create(
            customer=invoice_created.data.object.customer, 
            invoice=invoice_created.data.object.id, 
            currency='usd', 
            #amount=int(monthly_charge.charge_amount*100), 
            amount=500,
            description='# of reservations: %s Charge per Reservation: $%s Discount Amount: $%s' % (
                #ReservationCharge.objects.filter(monthly_charge_id=monthly_charge).count(), 
                #charge_profile.charge_per_reservation,
                #monthly_charge.discount_amount
                10,
                1.00,
                0.00
            )
        )
    return HttpResponse(status=200)

@login_required()
def edit_credit_card(request):
    client = request.user.profile.client
    return_url = '/charge/billing/' if request.GET.get('return_to_billing', False) else '/clients/update/'
    if request.method == "POST":

        # get the credit card details submitted by the form
        token = request.POST['stripeToken']
        
        # if the client doesn't have the stripe customer id defined, create a customer and store it.
        if client.charge_profile.stripe_customer_id == "":
            customer = stripe.Customer.create(
                card = token,
                description = client.contact_email
            )
            client.charge_profile.stripe_customer_id = customer.id
        elif token != "":
            customer = stripe.Customer.retrieve(client.charge_profile.stripe_customer_id)
            customer.card = token
            customer.save()
        request.session['show_confirmation'] = True
        request.session['confirmation_message'] = "Your credit card information was updated successfully!"
        return HttpResponseRedirect(return_url)
    
    token = stripe.Customer.retrieve(client.charge_profile.stripe_customer_id)['active_card'] if client.charge_profile.stripe_customer_id != "" else None 
    
    if token:
        card_number = ("*"*12) + token["last4"]
        month = token["exp_month"]
        year = token["exp_year"]
    else:
        card_number = ""
        month = ""
        year = ""
    
    return render_to_response('charge/edit_credit_card.html',
        {
            'return_to_billing': request.GET.get('return_to_billing', False),
            'stripe_pub_key': settings.STRIPE_PUB_KEY,
            'card_number': card_number,
            'month': month,
            'year': year,
            'client': client,
            'return_url': return_url
        },
        context_instance=RequestContext(request))

def get_session_value(request, key, delete):
    value = request.session.get(key)
    if delete:
        try:
            del request.session[key]
        except KeyError:
            pass
    return value
