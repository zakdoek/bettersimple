from django.conf.urls import patterns, include, url


urlpatterns = patterns('clientservice.views',
    url(r'^(?i)$','signup'),
    url(r'^(?i)signup/$', 'signup'),
    url(r'^(?i)(?P<client_id>\d+)/(?P<uuid>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})+)/$', 'detail'),
    url(r'^(?i)index/$', 'index'),
    url(r'^(?i)subscribe/$', 'subscribe'),
    url(r'^(?i)update/$', 'edit_client'),
    url(r'^(?i)stripeclientid/$','get_stripe_client_id'),
)
