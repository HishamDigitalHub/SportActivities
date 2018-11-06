from django.contrib import admin
from ActivityApp.models import Activity, ActivityImage, ActivityVideo, ActivityInvite, ActivityRating, \
    ActivityPreference


# Register your models here.


class ActivityAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['id', 'name', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_display_links = ['id', 'name']
    list_filter = ('name',)


class ActivityVideoAdmin(admin.ModelAdmin):
    search_fields = ['activity__name']
    list_display = ['id', 'get_activity', 'video', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_filter = ('activity__name',)

    def get_activity(self, obj):
        return obj.activity.name

    get_activity.short_description = 'Activity Name'
    get_activity.admin_order_field = 'activity__name'


class ActivityImageAdmin(admin.ModelAdmin):
    search_fields = ['activity__name']
    list_display = ['id', 'get_activity', 'image', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_filter = ('activity__name',)

    def get_activity(self, obj):
        return obj.activity.name

    get_activity.short_description = 'Activity Name'
    get_activity.admin_order_field = 'activity__name'


class ActivityRatingAdmin(admin.ModelAdmin):
    search_fields = ['activity__name', 'rate']
    list_display = ['id', 'get_activity', 'rate', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_display_links = ['get_activity', 'id']
    list_filter = ('activity__name', 'rate')

    def get_activity(self, obj):
        return obj.activity.name

    get_activity.short_description = 'Activity Name'
    get_activity.admin_order_field = 'activity__name'


class ActivityInviteAdmin(admin.ModelAdmin):
    search_fields = ['activity__name']
    list_display = ['id', 'get_activity', 'from_user', 'to_user', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_filter = ('activity__name',)

    def get_activity(self, obj):
        return obj.activity.name

    get_activity.short_description = 'Activity Name'
    get_activity.admin_order_field = 'activity__name'


class ActivityPreferenceAdmin(admin.ModelAdmin):
    search_fields = ['get_activity_name', 'get_activity_admin_name']
    list_display = ['id', 'get_activity_name', 'get_activity_admin_name']

    def get_activity_name(self, obj):
        return obj.activity.name

    def get_activity_admin_name(self, obj):
        return str(obj.activity.admin.first_name) + ' ' + str(obj.activity.admin.last_name)

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    get_activity_name.short_description = 'Activity Name'
    get_activity_admin_name.short_description = 'Activity Admin Name'
    get_activity_admin_name.admin_order_field = 'get_activity_name'


admin.site.register(Activity, ActivityAdmin)
admin.site.register(ActivityImage, ActivityImageAdmin)
admin.site.register(ActivityVideo, ActivityVideoAdmin)
admin.site.register(ActivityInvite, ActivityInviteAdmin)
admin.site.register(ActivityRating, ActivityRatingAdmin)
admin.site.register(ActivityPreference, ActivityPreferenceAdmin)
