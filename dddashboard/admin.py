from django.contrib import admin

# Register your models here.

from .models import *

# admin.site.register(Customer)
admin.site.register(Dashboard_user)
admin.site.register(CompanyData)
admin.site.register(CompanyName)
# admin.site.register(Tag)
# admin.site.register(Order)

