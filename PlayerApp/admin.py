from django.contrib import admin
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


admin.site.register(PlayerImage, PlayerImageAdmin)
admin.site.register(PlayerVideo, PlayerVideoAdmin)

