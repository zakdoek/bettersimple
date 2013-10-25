from django.conf.urls import patterns, include, url

from .views import signup, index, subscribe, edit_client, get_stripe_client_id, detail

urlpatterns = patterns(
    'clientservice.views',
    url(r'^(?i)$', signup, name='signup'),
    url(r'^(?i)signup/$', signup, name='signup_direct'),
    url(
        r'^(?i)(?P<client_id>\d+)/(?P<uuid>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})+)/$',
        detail, name='clientservice_detail'),
    url(r'^(?i)index/$', index, name='clientservice_index'),
    url(r'^(?i)subscribe/$', subscribe, name='subscribe'),
    url(r'^(?i)update/$', edit_client, name='edit_client'),
    url(r'^(?i)stripeclientid/$', get_stripe_client_id, name='get_stripe_client_id'),
)
