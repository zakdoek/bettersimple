from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?i)reservation/', include('reservation.urls')),
    url(r'^(?i)clients/', include('clientservice.urls')),
    #url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^(?i)accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^(?i)accounts/logout/$', 'clientservice.views.logout_view'),
    url(r'^(?i)support/', include('support.urls')),
    url(r'^(?i)message/', include('message.urls')),
    url(r'^(?i)charge/', include('charge.urls')),
    
    # Examples:
    # url(r'^$', 'bettersimple.views.home', name='home'),
    # url(r'^bettersimple/', include('bettersimple.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^(?i)admin/', include(admin.site.urls)),
    
    
    #set google domain ownership
    url(r'^google7e187a236424e7c8', direct_to_template, {
        'template': 'google7e187a236424e7c8.html'
    }),
    
    url(r'^(?i)sitemap.xml', direct_to_template, {
        'template': 'sitemap.xml', 
        'mimetype': 'application/xml'
    }),
    
    url(r'^(?i)demo', direct_to_template, {
        'template': 'demo.html'
    }),
    #Anything else goes to this page
    url(r'^$', direct_to_template, {
        'template': 'landing.html'
    }),
)
