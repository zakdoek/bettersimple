
from datetime import datetime, timedelta
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.utils import simplejson

import pytz

from message.models import *
from message.json.models import *
from message.send_sms import send_text

NUMBER_OF_MESSAGES_PER_ENDUSER_REQUEST = 50

@csrf_exempt
def get_enduser(request, token):
    if settings.EMAIL_TOKEN != token:
        raise Http404
    if request.method == "POST":
        # update any sent messages. Shouldn't allow any non-pending messages be modified.
               
        for message_id in request.POST.getlist('ids-sent', []):
            message = Message.objects.get(Q(pk=message_id), Q(status=Message.PENDING), enduser_message_type_query())
            message.status = Message.SENT
            message.save()
        # update any errored messages. Shouldn't allow any non-pending messages be modified.
        for message_id in request.POST.getlist('ids-error', []):
            message = Message.objects.get(Q(pk=message_id), Q(status=Message.PENDING), enduser_message_type_query())
            message.status = Message.ERROR
            message.save()
        # for all messages that have been pending for an hour, set it back to unsent so it gets sent again.
        for message in Message.objects.filter(Q(status=Message.PENDING), Q(send_datetime__lt=datetime.utcnow().replace(tzinfo=pytz.UTC) - timedelta(hours=1)),
            enduser_message_type_query()):
            message.status = Message.UNSENT
            message.save()
        return HttpResponse(simplejson.dumps({'success':True}), mimetype='application/javascript')
    else: #GET
        texts = Message.objects.filter(Q(status=Message.UNSENT), Q(send_datetime__lt=datetime.utcnow().replace(tzinfo=pytz.UTC, minute=59, second=59, microsecond=59)),
            Q(message_type=Message.RESERVATION_REMINDER_TEXT))
        for message in texts:
            send_text( '9202537828', get_text_message_reminder(message.reservation)) # message.reservation.customer.phone
            message.status = Message.SENT
            message.save()
        # fetch reservation specific messages that are unsent that are to be sent for this hour.
        messages = Message.objects.filter(Q(status=Message.UNSENT), Q(send_datetime__lt=datetime.utcnow().replace(tzinfo=pytz.UTC, minute=59, second=59, microsecond=59)),
            enduser_message_type_query())
        contract_messages = []
        # update all messages to pending
        for message in messages:
            message.status = Message.PENDING
            message.save()
            # return messages in JSON format
            contract_messages.append(ContractMessage.create(message=message).__dict__)
        return HttpResponse(simplejson.dumps(contract_messages), mimetype='application/javascript')

@csrf_exempt
def get_company_report(request, token):
    if settings.EMAIL_TOKEN != token:
        raise Http404
    if request.method == "POST":
        for message_id in request.POST.getlist('ids-sent', []):
            message = Message.objects.get(pk=message_id, message_type=Message.RESERVATION_COMPANY_REPORT, status=Message.PENDING)
            message.status = Message.SENT
            message.save()
        # update any errored messages. Shouldn't allow any non-pending messages be modified.
        for message_id in request.POST.getlist('ids-error', []):
            message = Message.objects.get(pk=message_id, message_type=Message.RESERVATION_COMPANY_REPORT, status=Message.PENDING)
            message.status = Message.ERROR
            message.save()
        # for all messages that have been pending for an hour, set it back to unsent so it gets sent again.
        for message in Message.objects.filter(status=Message.PENDING, send_datetime__lt=(datetime.utcnow().replace(tzinfo=pytz.UTC) - timedelta(hours=1)),
            message_type=Message.RESERVATION_COMPANY_REPORT):
            message.status = Message.UNSENT
            message.save()
        return HttpResponse(simplejson.dumps({'success':True}), mimetype='application/javascript')
    else:
        # Get the last sent company report for each client
        last_reports_sent = Message.objects.filter(Q(status=Message.PENDING) | Q(status=Message.SENT) | Q(status=Message.UNSENT),
            Q(message_type=Message.RESERVATION_COMPANY_REPORT)).order_by('client', '-send_datetime').distinct('client')
        
        clients_sent_reports_today = []
        # get the local time for today
        # create a list of clients that have sent reports out today already
        for msg in last_reports_sent:
            if msg.client.local_now().replace(hour=0,minute=0,second=0,microsecond=0) <= msg.client.localize(msg.send_datetime) <= msg.client.local_now().replace(hour=23,minute=59,second=59,microsecond=999999):
                clients_sent_reports_today.append(msg.client)
        
        # build up a query that will exclude all of the clients that already have sent company reports
        clients = Client.objects.all()
        for client in clients_sent_reports_today:
            clients = clients.exclude(id=client.id)
        
        messages = []
        for message in last_reports_sent:
            if message.status == Message.UNSENT:
                message.status = Message.PENDING
                message.save()
                messages.append(message)
                
        for client in clients:
            message = Message()
            message.client = client
            message.status = Message.PENDING
            message.message_type = Message.RESERVATION_COMPANY_REPORT
            message.send_datetime = datetime.utcnow().replace(tzinfo=pytz.UTC)
            message.save()
            messages.append(message)
            
        # return messages in JSON format
        contract_messages = [ContractMessage.create(message=message).__dict__ for message in messages]
        return HttpResponse(simplejson.dumps(contract_messages), mimetype='application/javascript')

@csrf_exempt
def get_monthly_charge(request, token):
    if settings.EMAIL_TOKEN != token:
        raise Http404
    if request.method == "POST":
        for message_id in request.POST.getlist('ids-sent', []):
            message = Message.objects.get(pk=message_id, message_type=Message.CLIENT_MONTHLY_CHARGE, status=Message.PENDING)
            message.status = Message.SENT
            message.save()
            if not message.monthly_charge.paid:
                # create a message to be sent out next week.
                next_weeks_msg = Message.create_monthly_charge(message.monthly_charge)
                next_weeks_msg.send_datetime = next_weeks_msg.send_datetime + timedelta(weeks=1)
                next_weeks_msg.save()
                
        # update any errored messages. Shouldn't allow any non-pending messages be modified.
        for message_id in request.POST.getlist('ids-error', []):
            message = Message.objects.get(pk=message_id, message_type=Message.CLIENT_MONTHLY_CHARGE, status=Message.PENDING)
            message.status = Message.ERROR
            message.save()
        # for all messages that have been pending for an hour, set it back to unsent so it gets sent again.
        for message in Message.objects.filter(status=Message.PENDING, send_datetime__lt=(datetime.utcnow().replace(tzinfo=pytz.UTC) - timedelta(hours=1)),
            message_type=Message.CLIENT_MONTHLY_CHARGE):
            message.status = Message.UNSENT
            message.save()
        return HttpResponse(simplejson.dumps({'success':True}), mimetype='application/javascript')
    else:
        # Get the unsent monthly bills
        messages = Message.objects.filter(Q(status=Message.UNSENT), Q(send_datetime__lt=datetime.utcnow().replace(tzinfo=pytz.UTC, minute=59, second=59, microsecond=59)),
            Q(message_type=Message.CLIENT_MONTHLY_CHARGE))
        contract_messages = []
        # update all messages to pending
        for message in messages:
            message.status = Message.PENDING
            message.save()
            # return messages in JSON format
            contract_messages.append(ContractMessage.create(message=message).__dict__)
        return HttpResponse(simplejson.dumps(contract_messages), mimetype='application/javascript')
        
def enduser_message_type_query():
    return (
        Q(message_type=Message.RESERVATION_CREATE_CONFIRM) | 
        Q(message_type=Message.RESERVATION_UPDATE_CONFIRM) | 
        Q(message_type=Message.RESERVATION_REMINDER) |
        Q(message_type=Message.RESERVATION_DELETED) |
        Q(message_type=Message.CLIENT_CREATE_CONFIRM) |
        Q(message_type=Message.CLIENT_UPDATE_CONFIRM) 
    )
