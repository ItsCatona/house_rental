from django.contrib import admin
from rental_system.models import Tenant, Payment
from rental_system.models import Property

# Register your models here.
admin.site.register(Tenant)
admin.site.register(Property)
admin.site.register(Payment)