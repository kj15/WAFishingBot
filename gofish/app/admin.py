from django.contrib import admin

from .models import Lake, Fish, County, StockingData, LakeStats

# Register your models here.

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'

@admin.register(Lake)
class LakeAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'url', 'rank', 'size', 'altitude', 'county', 'get_stocking')
    list_filter = ['county']
    ordering = ['county']

    def get_stocking(self, obj):
        return "\n".join(["[" + str(a.date) + "] : " + str(a.amount) for a in StockingData.objects.all().filter(lake=obj)])


@admin.register(LakeStats)
class LakeStatsAdmin(admin.ModelAdmin):
    list_display = ('last_updated', 'total', 'min_size', 'avg_size', 'max_size', 'min_alt', 'avg_alt', 'max_alt')

admin.site.register(Fish)
admin.site.register(County)
admin.site.register(StockingData)