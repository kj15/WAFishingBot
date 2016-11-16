from django.contrib import admin

from .models import Lake, Fish, County, StockingData

# Register your models here.

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'

@admin.register(Lake)
class LakeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'url', 'rank', 'county', 'get_stocking')
    list_filter = ['county']
    ordering = ['county']

    def get_stocking(self, obj):
        return "\n".join(["[" + str(a.date) + "] : " + str(a.amount) for a in StockingData.objects.all().filter(lake=obj)])

admin.site.register(Fish)
admin.site.register(County)
admin.site.register(StockingData)