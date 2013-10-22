from django.conf.urls import patterns, include, url

urlpatterns = patterns('reservation.views',
    url(r'^(?i)$', 'index'),
    url(r'^(?i)(?P<reservation_id>\d+)/$', 'detail'),
    url(r'^(?i)update/(?P<reservation_id>\d+)/$', 'edit_reservation'),
    #url(r'^(?i)update/(?P<reservation_id>\d+)/(?P<uuid>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})+)/$', 'user_edit'),
    #url(r'^(?i)create/(?P<client_id>\d+)/(?P<company_uuid>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})+)/$', 'user_create_reservation'),
    url(r'^(?i)create/$', 'create_reservation'),
    url(r'^(?i)(?P<reservation_id>\d+)/(?P<uuid>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})+)/delete/$', 'delete_reservation'),
    url(r'^(?i)download/', 'download_to_csv'),
)
