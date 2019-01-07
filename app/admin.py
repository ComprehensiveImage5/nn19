from django.contrib import admin

from .models import CheckIn, Soldier

# Register your models here.
admin.site.register(CheckIn)
admin.site.register(Soldier)

admin.site.site_title = 'NoNut19'
admin.site.site_header = 'Admin Page'