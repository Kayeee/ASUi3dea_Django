from django.contrib import admin

from .models import *
#
# # Register your models here.
admin.site.register(Inverter)
admin.site.register(Pi)
admin.site.register(Temperature)
admin.site.register(Mode)
