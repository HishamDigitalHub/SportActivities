from django.contrib import admin

from Global_Functions.admin_panel import AfterSave
from PlayerApp.models import PlayerImage, PlayerVideo
# Register your models here.


# class TeamAdmin(admin.ModelAdmin):
#     search_fields = ['name']
#     list_display = ['name']
#     list_filter = ('name',)


class PlayerVideoAdmin(admin.ModelAdmin):
    search_fields = ['Player__name']
    list_display = ['get_player', 'get_user', 'video']
    list_filter = ('user__username',)

    def get_player(self, obj):
        full_name = obj.user.first_name + ' ' + obj.user.last_name
        return full_name
    get_player.short_description = 'Player Name'
    get_player.admin_order_field = 'user__first_name'

    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'User Name'

    def save_model(self, request, obj, form, change):
        AfterSave.save_model(self=self, request=request, obj=obj, form=form, change=change)


class PlayerImageAdmin(admin.ModelAdmin):
    search_fields = ['team__name']
    list_display = ['get_player', 'get_user', 'image']
    list_filter = ('user__username',)

    def get_player(self, obj):
        full_name = obj.user.first_name + ' ' + obj.user.last_name
        return full_name
    get_player.short_description = 'Player Name'
    get_player.admin_order_field = 'user__first_name'

    def get_user(self, obj):
        return obj.user.username
    get_user.short_description = 'User Name'

    def save_model(self, request, obj, form, change):
        AfterSave.save_model(self=self, request=request, obj=obj, form=form, change=change)

admin.site.register(PlayerImage, PlayerImageAdmin)
admin.site.register(PlayerVideo, PlayerVideoAdmin)

