from django.conf import settings
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db import IntegrityError


class TimezoneMiddleware(object):
    def process_request(self, request):
        #tz = request.session.get('django_timezone')
        #if tz:
        #this neds to get changed
        if request.user.is_anonymous():
            timezone.activate(settings.TIME_ZONE)
        else:
            try:
                if request.user.profile:
                    timezone.activate(request.user.profile.client.timezone_name)
            except IntegrityError:
                timezone.activate(settings.TIME_ZONE)


class SSLMiddleware(object):
    def process_request(self, request):
        if request.META['SERVER_PORT'] != "25" and request.META['SERVER_PORT'] != "587" and not any([settings.DEBUG, request.is_secure(), request.META.get("HTTP_X_FORWARDED_PROTO", "") == 'https']):
            url = request.build_absolute_uri(request.get_full_path())
			# Hack for allowing IE cross domain ajax requests. If the page hosting the ajax call is http, the response must be http not https
            if url.find('/reservation/create/') == -1 and url.find('robots.txt') == -1 and url.find('sitemap.xml') == -1:
                secure_url = url.replace("http://", "https://")
                return HttpResponseRedirect(secure_url)

class CrossOriginMiddleware(object):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = "*"
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type, x-requested-with, Content-Length, accept, Host, Origin, Refer, User-Agent, Connection'
            
        return response
