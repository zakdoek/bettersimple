from django.contrib import admin
from message.models import *

class MessageAdmin(admin.ModelAdmin):
    pass

   
admin.site.register(Message, MessageAdmin)
