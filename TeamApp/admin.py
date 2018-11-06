from django.contrib import admin
from TeamApp.models import Team, TeamImage, TeamVideo, TeamInvite, TeamPreference

# Register your models here.


class TeamAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['id', 'name', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_display_links = ['id', 'name']
    list_filter = ('name',)


class TeamVideoAdmin(admin.ModelAdmin):
    search_fields = ['team__name']
    list_display = ['get_team', 'video', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_filter = ('team__name',)

    def get_team(self, obj):
        return obj.team.name
    get_team.short_description = 'Team Name'
    get_team.admin_order_field = 'team__name'


class TeamImageAdmin(admin.ModelAdmin):
    search_fields = ['team__name']
    list_display = ['get_team', 'image', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_filter = ('team__name',)

    def get_team(self, obj):
        return obj.team.name
    get_team.short_description = 'Team Name'
    get_team.admin_order_field = 'team__name'


class TeamInviteAdmin(admin.ModelAdmin):
    search_fields = ['team__name']
    list_display = ['id', 'get_team', 'from_user', 'to_user', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_filter = ('team__name',)

    def get_team(self, obj):
        return obj.activity.name

    get_team.short_description = 'Team Name'
    get_team.admin_order_field = 'team__name'


class TeamPreferenceAdmin(admin.ModelAdmin):
    search_fields = ['get_team_name', 'get_team_admin_name']
    list_display = ['id', 'get_team_name', 'get_team_admin_name']

    def get_team_name(self, obj):
        return obj.team.name

    def get_team_admin_name(self, obj):
        return str(obj.team.admin.first_name) + ' ' + str(obj.team.admin.last_name)

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    get_team_name.short_description = 'Team Name'
    get_team_admin_name.short_description = 'Team Admin Name'
    get_team_admin_name.admin_order_field = 'get_team_name'


admin.site.register(Team, TeamAdmin)
admin.site.register(TeamImage, TeamImageAdmin)
admin.site.register(TeamVideo, TeamVideoAdmin)
admin.site.register(TeamInvite, TeamInviteAdmin)
admin.site.register(TeamPreference, TeamPreferenceAdmin)

# class ActivityRatingAdmin(admin.ModelAdmin):
#     search_fields = ['activity__name', 'rate']
#     list_display = ['id', 'get_activity', 'rate', 'updated_date', 'created_date', 'created_by', 'updated_by']
#     list_display_links = ['get_activity', 'id']
#     list_filter = ('activity__name', 'rate')
#
#     def get_activity(self, obj):
#         return obj.activity.name
#
#     get_activity.short_description = 'Activity Name'
#     get_activity.admin_order_field = 'activity__name'
#
#
