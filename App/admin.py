from django.contrib import admin
from .models import Products, User, Events, Pay

admin.site.register(Products)
admin.site.register(Events)
admin.site.register(User)
admin.site.register(Pay)