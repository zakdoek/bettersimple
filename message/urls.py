from django.conf.urls import patterns, include, url


urlpatterns = patterns('message.views',
    url(r'^(?i)api/enduser/(?P<token>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})+)/$','get_enduser'),
    url(r'^(?i)api/companyreport/(?P<token>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})+)/$','get_company_report'),
    url(r'^(?i)api/monthlycharge/(?P<token>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})+)/$','get_monthly_charge'),
)
