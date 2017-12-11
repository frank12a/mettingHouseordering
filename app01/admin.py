from django.contrib import admin
from . import  models

# Register your models here.
admin.site.register(models.Userinfo)
admin.site.register(models.Bookings)
admin.site.register(models.Room)
