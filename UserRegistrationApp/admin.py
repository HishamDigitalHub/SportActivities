from django.contrib import admin

from Global_Functions.admin_panel import AfterSave
from .models import Profile, User, UserPreference


# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    list_display = ['id', 'get_user_id', 'get_user', 'get_first_name', 'get_last_name']
    # list_display_links = ['id', 'name']
    # list_filter = ('user_username', 'user__first_name', 'user__last_name')

    def get_user(self, obj):
        return obj.user.username

    def get_user_id(self, obj):
        return obj.user.id

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    get_user.short_description = 'UserName'
    get_user.admin_order_field = 'user__name'

    def save_model(self, request, obj, form, change):
        AfterSave.save_model(self=self, request=request, obj=obj, form=form, change=change)

class UserPreferenceAdmin(admin.ModelAdmin):
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    list_display = ['id', 'get_user_id', 'get_user', 'get_first_name', 'get_last_name']

    def get_user(self, obj):
        return obj.user.username

    def get_user_id(self, obj):
        return obj.user.id

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    get_user.short_description = 'UserName'
    get_user.admin_order_field = 'user__name'

    def save_model(self, request, obj, form, change):
        AfterSave.save_model(self=self, request=request, obj=obj, form=form, change=change)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserPreference, UserPreferenceAdmin)

