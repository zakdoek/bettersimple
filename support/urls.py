from django.conf.urls import patterns, include, url

from .views import about_us, setup

urlpatterns = patterns(
    'support.views',
    url(r'^(?i)aboutus', about_us, name='about_us'),
    url(r'^(?i)setup', setup, name='setup_direct'),
    url(r'^', setup, name='setup'),
)
