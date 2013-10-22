
from django.conf import settings
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.utils import simplejson
import stripe

from clientservice.models import *
from clientservice.forms import *
from message.models import *
from charge.models import *
from django.db import connection, transaction

@login_required()
def index(request):
    # Display the clients
    clients = Client.objects.all()
    return render_to_response('clients/index.html', {'clients': clients},context_instance=RequestContext(request))

def detail(request, client_id, uuid):
    client = get_object_or_404(Client, id=client_id, uuid=uuid)
    code = ClientCode.objects.filter(client_id=client_id)[0]
    return render_to_response('clients/detail.html', {'client_code': code},context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/support/setup')
    client = Client()
    
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        user_form = RegistrationForm(request.POST)
        industry_profile_form = IndustryProfileForm(request.POST)
        if client_form.is_valid() and user_form.is_valid() and industry_profile_form.is_valid():
            user = user_form.save()
            industry_profile = industry_profile_form.save()
            client = client_form.save(commit = False)
            charge_profile = ClientChargeProfile()
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe_customer = stripe.Customer.create(plan='reservation-basic', email=client.contact_email, description=("Client ID: %s Name: %s" % (client.id, client.name)))
            charge_profile.stripe_customer_id = stripe_customer["id"]
            charge_profile.save()
            client.charge_profile = charge_profile
            client.industry_profile = industry_profile
            client.save()
            client_form.save_m2m()
            client_code = ClientCode()
            client_code.client = client
            client_code.save()
            profile = UserProfile()
            profile.client = client
            profile.user = user
            profile.save()
            client_code.set_defaults()
            # log the user in
            new_user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, new_user)
            Message.create_client_message(client, Message.CLIENT_CREATE_CONFIRM)
            return HttpResponseRedirect('/support/setup')
            
    else:
        client_form = ClientForm(instance=Client())
        user_form = RegistrationForm()
        industry_profile_form = IndustryProfileForm()
    
    return render_to_response('clients/signup.html', 
        {
            'client': client,
            'client_form': client_form,
            'user_form': user_form,
            'industry_profile_form': industry_profile_form,
        }, 
        context_instance=RequestContext(request))
    
def subscribe(request):
    if request.method == "POST":
        potentialclient_form = PotentialClientForm(request.POST)
        # only create a new one if it hasn't already been created.
        # todo -> make this case insensitive.
        if not potentialclient_form.is_valid():
            return HttpResponse(simplejson.dumps({'formattedCorrectly':False, 'created':False}), mimetype='application/javascript')
        if not PotentialClient.objects.filter(email__iexact = potentialclient_form['email'].value()).count() == 0:
            return HttpResponse(simplejson.dumps({'formattedCorrectly':True, 'created':False}), mimetype='application/javascript')
        potentialclient_form.save()
        return HttpResponse(simplejson.dumps({'formattedCorrectly':True, 'created':True}), mimetype='application/javascript')
    # if we get to here it wasn't created
    return HttpResponse(simplejson.dumps({'created':False}), mimetype='application/javascript')
        

@login_required()
def edit_client(request):
    client = request.user.profile.client
    show_confirmation = get_session_value(request, "show_confirmation", True)
    confirmation_message = get_session_value(request, "confirmation_message", True)
    if request.method == "POST":
        client_form = ClientForm(request.POST, instance=client)
        industry_profile_form = IndustryProfileForm(request.POST, instance=client.industry_profile)
        if client_form.is_valid() and industry_profile_form.is_valid():
            industry_profile = industry_profile_form.save()
            client = client_form.save(commit = False)  
            client.industry_profile = industry_profile
            client.save()
            client_form.save_m2m()
            # regenerate the client code.  
            code = client.clientcode
            code.save()
            code.set_defaults()
            code.save()
            # refetch the client.
            client = Client.objects.get(pk=client.id)
            if client.charge_profile.stripe_customer_id != "":
                # update stripe's email
                stripe_customer = stripe.Customer.retrieve(client.charge_profile.stripe_customer_id)
                stripe_customer.email = client.contact_email
                stripe_customer.description = "Client ID: %s Name: %s" % (client.id, client.name)
                stripe_customer.save()
            else:
                # if a stripe customer hasn't been created, then go ahead and create one!
                stripe_customer = stripe.Customer.create(plan='reservation-basic', email=client.contact_email, description=("Client ID: %s Name: %s" % (client.id, client.name)))
                client.charge_profile.stripe_customer_id = stripe_customer["id"]
                client.charge_profile.save()
                
            Message.create_client_message(client, Message.CLIENT_UPDATE_CONFIRM)
            
            try:
                show_credit_alert = (client.charge_profile.stripe_customer_id == "" or stripe.Customer.retrieve(client.charge_profile.stripe_customer_id)["active_card"] == None)
            except KeyError:
                show_credit_alert = True
            return render_to_response('clients/update.html', 
                {
                    'client_form' : client_form, 
                    'industry_profile_form': industry_profile_form,
                    'client':client, 
                    'show_confirmation': True,
                    'confirmation_message': 'Your changes have been saved successfully!',
                    'show_credit_alert': show_credit_alert
                },
                context_instance=RequestContext(request))
    else:
        client_form = ClientForm(instance=client)
        industry_profile_form = IndustryProfileForm(instance=client.industry_profile)
        
    return render_to_response('clients/update.html', 
        {
            'client_form' : client_form, 
            'industry_profile_form': industry_profile_form,
            'client':client, 
            'show_confirmation': show_confirmation,
            'confirmation_message': confirmation_message,
            'stripe_customer_id': client.charge_profile.stripe_customer_id
        },
        context_instance=RequestContext(request))

@login_required()
def get_stripe_client_id(request):
    
    client = request.user.profile.client
    client_id = client.charge_profile.stripe_customer_id if client.charge_profile.stripe_customer_id == "" else ( 
            stripe.Customer.retrieve(client.charge_profile.stripe_customer_id)["active_card"]["last4"] )
    
    return HttpResponse(simplejson.dumps({'hasCard':client_id != ""}), mimetype='application/javascript')
    
def get_session_value(request, key, delete):
    value = request.session.get(key)
    if delete:
        try:
            del request.session[key]
        except KeyError:
            pass
    return value
