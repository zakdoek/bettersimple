from django.contrib import admin
from clientservice.models import *

class ClientAdmin(admin.ModelAdmin):
    pass

class ClientCodeAdmin(admin.ModelAdmin):
    pass
    
class UserProfileAdmin(admin.ModelAdmin):
    pass
    
class IndustryProfileAdmin(admin.ModelAdmin):
    pass
    
class PotentialClientAdmin(admin.ModelAdmin):
    pass
   
admin.site.register(Client, ClientAdmin)
admin.site.register(ClientCode, ClientCodeAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(IndustryProfile, IndustryProfileAdmin)
admin.site.register(PotentialClient, PotentialClientAdmin)
