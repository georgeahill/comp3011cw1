from django.contrib import admin
from .models import Module, Professor, Teaching, Rating

admin.site.register(Module)
admin.site.register(Professor)
admin.site.register(Teaching)
admin.site.register(Rating)