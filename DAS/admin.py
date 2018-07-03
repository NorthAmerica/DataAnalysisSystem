from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Statement)

admin.site.register(Position_Detail)

admin.site.register(Position_Summary)

admin.site.register(Trading_Detail)

admin.site.register(Close_Detail)