from django.conf.urls import patterns, include, url


urlpatterns = patterns('support.views',
    url(r'^(?i)aboutus','about_us'),
    url(r'^(?i)setup','setup'),
    url(r'^', 'setup'),
)
