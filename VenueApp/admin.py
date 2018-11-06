from django.contrib import admin
from VenueApp.models import Venue, VenueImage, VenueVideo, VenueRating, VenuePreference


# Register your models here.


class VenueAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['id', 'name', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_display_links = ['id', 'name']
    list_filter = ('name',)


class VenueVideoAdmin(admin.ModelAdmin):
    search_fields = ['venue__name']
    list_display = ['id', 'get_venue', 'video', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_filter = ('venue__name',)

    def get_venue(self, obj):
        return obj.venue.name

    get_venue.short_description = 'Venue Name'
    get_venue.admin_order_field = 'venue__name'


class VenueImageAdmin(admin.ModelAdmin):
    search_fields = ['venue__name']
    list_display = ['id', 'get_venue', 'image', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_filter = ('venue__name',)

    def get_venue(self, obj):
        return obj.venue.name

    get_venue.short_description = 'Venue Name'
    get_venue.admin_order_field = 'venue__name'


class VenueRatingAdmin(admin.ModelAdmin):
    search_fields = ['venue__name', 'rate']
    list_display = ['id', 'get_venue', 'rate', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_display_links = ['get_venue', 'id']
    list_filter = ('venue__name', 'rate')

    def get_venue(self, obj):
        return obj.venue.name

    get_venue.short_description = 'Venue Name'
    get_venue.admin_order_field = 'venue__name'


class VenuePreferenceAdmin(admin.ModelAdmin):
    search_fields = ['get_venue_name', 'get_venue_admin_name']
    list_display = ['id', 'get_venue_name', 'get_venue_admin_name']

    def get_venue_name(self, obj):
        return obj.venue.name

    def get_venue_admin_name(self, obj):
        return str(obj.venue.admin.first_name) + ' ' + str(obj.venue.admin.last_name)

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    get_venue_name.short_description = 'Venue Name'
    get_venue_admin_name.short_description = 'Venue Admin Name'
    get_venue_admin_name.admin_order_field = 'get_venue_name'


admin.site.register(Venue, VenueAdmin)
admin.site.register(VenueImage, VenueImageAdmin)
admin.site.register(VenueVideo, VenueVideoAdmin)
admin.site.register(VenueRating, VenueRatingAdmin)
admin.site.register(VenuePreference, VenuePreferenceAdmin)
