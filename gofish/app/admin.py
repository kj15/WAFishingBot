from django.contrib import admin

from .models import Lake, Fish, County, StockingData

# Register your models here.
admin.site.register(Lake)
admin.site.register(Fish)
admin.site.register(County)
admin.site.register(StockingData)