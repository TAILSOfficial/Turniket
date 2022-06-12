from django.contrib import admin

from .models import leader, member


admin.site.register(leader)
admin.site.register(member)