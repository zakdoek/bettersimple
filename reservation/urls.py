from django.conf.urls import patterns, include, url

from views.base import index, detail, edit_reservation, delete_reservation, create_reservation, download_to_csv
from views.create import user_create_reservation_appointment
from views.edit import user_edit_appointment

urlpatterns = patterns(
    'reservation.views',
    url(r'^(?i)$', index, name='reservation_index'),
    url(r'^(?i)(?P<reservation_id>\d+)/$', detail, name='reservation_detail'),
    url(r'^(?i)update/(?P<reservation_id>\d+)/$', edit_reservation, name='edit_reservation'),
    url(r'^(?i)update/(?P<reservation_id>\d+)/(?P<uuid>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})+)/$',
        user_edit_appointment, name='user_edit_appointment'),
    url(r'^(?i)create/(?P<client_id>\d+)/(?P<company_uuid>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})+)/$',
        user_create_reservation_appointment, name='user_create_reservation_appointment'),
    url(r'^(?i)create/$', create_reservation, name='create_reservation'),
    url(r'^(?i)(?P<reservation_id>\d+)/(?P<uuid>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})+)/delete/$',
        delete_reservation, name='delete_reservation'),
    url(r'^(?i)download/', download_to_csv, name='download_to_csv'),
)
