from django.contrib import admin
from charge.models import ClientChargeProfile, MonthlyCharge, ReservationCharge, MessageCharge

class ClientChargeProfileAdmin(admin.ModelAdmin):
    pass

class MonthlyChargeAdmin(admin.ModelAdmin):
    pass
    
class ReservationChargeAdmin(admin.ModelAdmin):
    pass

class MessageChargeAdmin(admin.ModelAdmin):
    pass

admin.site.register(ClientChargeProfile, ClientChargeProfileAdmin)
admin.site.register(MonthlyCharge, MonthlyChargeAdmin)
admin.site.register(ReservationCharge, ReservationChargeAdmin)
admin.site.register(MessageCharge, MessageChargeAdmin)