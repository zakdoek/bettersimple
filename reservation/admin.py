from django.contrib import admin
from reservation.models import *

class ReservationAdmin(admin.ModelAdmin):
    pass
    
class TripAdmin(admin.ModelAdmin):
    pass

class AddressAdmin(admin.ModelAdmin):
    pass

class ClientLandmarkAdmin(admin.ModelAdmin):
    pass
    
class ContactAdmin(admin.ModelAdmin):
    pass
   
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(ClientLandmark, ClientLandmarkAdmin)
