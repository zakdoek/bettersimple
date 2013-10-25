from django.conf.urls import patterns, include, url

from .views import get_enduser, get_company_report, get_monthly_charge

urlpatterns = patterns(
    'message.views',
    url(r'^(?i)api/enduser/(?P<token>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})+)/$',
        get_enduser, name='get_enduser'),
    url(r'^(?i)api/companyreport/(?P<token>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})+)/$',
        get_company_report, name='get_company_report'),
    url(r'^(?i)api/monthlycharge/(?P<token>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})+)/$',
        get_monthly_charge, name='get_monthly_charge'),
)
