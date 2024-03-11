from django.contrib import admin

from services.models import Plan, Service, Subscription


admin.site.register(Service)
admin.site.register(Subscription)
admin.site.register(Plan)
