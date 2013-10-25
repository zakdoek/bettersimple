from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse

from clientservice.models import ClientCode


def about_us(request):
    # Display the about us page
    return render_to_response('support/aboutus.html', {},context_instance=RequestContext(request))


def setup(request):
    client_code = get_object_or_404(ClientCode, client_id=request.user.profile.client.id)
    return render_to_response('support/setup.html', {'client_code':client_code},context_instance=RequestContext(request))

