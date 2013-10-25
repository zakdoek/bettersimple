from django.conf.urls import patterns, include, url
from .views import edit_credit_card, billing, past_charge, stripe_webhook, process_monthly_charges

urlpatterns = patterns(
    'charge.views',
    url(r'^(?i)creditcard', edit_credit_card, name="edit_card_card"),
    url(r'^(?i)billing', billing, name="billing"),
    url(r'^(?i)past_charge/(\d{4})/(\d{2})/$', past_charge, name='past_charge'),
    url(
        r'^(?i)api/stripe_webhook/(?P<token>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})+)/$',
        stripe_webhook, name='stripe_webhook'),
    url(
        r'^(?i)api/process_monthly_charges/(?P<token>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})+)/$',
        process_monthly_charges, name='process_monthly_charges'),
)
