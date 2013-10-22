from django.conf.urls import patterns, include, url


urlpatterns = patterns('charge.views',
    url(r'^(?i)creditcard','edit_credit_card'),
    url(r'^(?i)billing','billing'),
    url(r'^(?i)past_charge/(\d{4})/(\d{2})/$', 'past_charge'),
    url(r'^(?i)api/stripe_webhook/(?P<token>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})+)/$','stripe_webhook'),
    url(r'^(?i)api/process_monthly_charges/(?P<token>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})+)/$','process_monthly_charges'),
)
