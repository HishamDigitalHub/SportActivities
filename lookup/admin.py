from django.contrib import admin
from .models import Country, City, SportIcon, Sport
# Register your models here.


class CountryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['name', 'icon']
    list_filter = ('name',)


admin.site.register(Country, CountryAdmin)


class CityAdmin(admin.ModelAdmin):
    search_fields = ['name', 'country__name']
    list_display = ['name', 'country']
    list_filter = ('country__name', 'name',)


class SportAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['id', 'name', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_display_links = ['id', 'name']
    list_filter = ('name',)


class SportIconAdmin(admin.ModelAdmin):
    search_fields = ['sport_name']
    list_display = ['get_sport', 'updated_date', 'created_date', 'created_by', 'updated_by']
    # list_display_links = ['id', 'get_sport']
    list_filter = ('sport__name',)

    def get_sport(self, obj):
        return obj.sport.name

    get_sport.short_description = 'Sport Name'
    get_sport.admin_order_field = 'sport__name'


admin.site.register(City, CityAdmin)
admin.site.register(Sport, SportAdmin)
admin.site.register(SportIcon, SportIconAdmin)
