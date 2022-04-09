from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *
# Register your models here.
admin.site.unregister(Group)
admin.site.register(Notification)
admin.site.register(Ad)

admin.site.site_header = 'ADMIN SITE'