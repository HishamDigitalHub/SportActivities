from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.timezone import now
from Global_Functions.admin_panel import AfterSave
from FitnessApp.models import (Fitness,
                               Workout,
                               ExerciseIcon,
                               ExerciseImage,
                               Exercise,
                               ExerciseRating,
                               ExerciseVideo)

# Register your models here.


class ExerciseAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['id', 'name', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_display_links = ['id', 'name']
    list_filter = ('name',)

    def save_model(self, request, obj, form, change):
        AfterSave.save_model(self=self, request=request, obj=obj, form=form, change=change)


class WorkoutAdmin(admin.ModelAdmin):
    search_fields = ['admin']
    list_display = ['id', 'admin', 'appointment', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_display_links = ['id', 'admin']
    list_filter = ('admin',)

    def save_model(self, request, obj, form, change):
        AfterSave.save_model(self=self, request=request, obj=obj, form=form, change=change)

class ExerciseVideoAdmin(admin.ModelAdmin):
    search_fields = ['exercise__name']
    list_display = ['id', 'get_exercise', 'video', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_filter = ('exercise__name',)

    def get_exercise(self, obj):
        return obj.exercise.name

    get_exercise.short_description = 'Exercise Name'
    get_exercise.admin_order_field = 'exercise__name'

    def save_model(self, request, obj, form, change):
        AfterSave.save_model(self=self, request=request, obj=obj, form=form, change=change)

class ExerciseImageAdmin(admin.ModelAdmin):
    search_fields = ['exercise__name']
    list_display = ['id', 'get_exercise', 'image', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_filter = ('exercise__name',)

    def get_exercise(self, obj):
        return obj.exercise.name

    get_exercise.short_description = 'Exercise Name'
    get_exercise.admin_order_field = 'exercise__name'

    def save_model(self, request, obj, form, change):
        AfterSave.save_model(self=self, request=request, obj=obj, form=form, change=change)

class ExerciseRatingAdmin(admin.ModelAdmin):
    search_fields = ['exercise__name', 'rate']
    list_display = ['id', 'get_exercise', 'rate', 'updated_date', 'created_date', 'created_by', 'updated_by']
    list_display_links = ['get_exercise', 'id']
    list_filter = ('exercise__name', 'rate')

    def get_exercise(self, obj):
        return obj.exercise.name

    get_exercise.short_description = 'Exercise Name'
    get_exercise.admin_order_field = 'exercise__name'

    def save_model(self, request, obj, form, change):
        AfterSave.save_model(self=self, request=request, obj=obj, form=form, change=change)

class ExerciseIconAdmin(admin.ModelAdmin):
    search_fields = ['exercise__name', 'rate']
    list_display = ['get_exercise', 'updated_date', 'created_date', 'created_by', 'updated_by']
    # list_display_links = ['id', 'get_sport']
    list_filter = ('exercise__name',)

    def get_exercise(self, obj):
        return obj.exercise.name

    get_exercise.short_description = 'Exercise Name'
    get_exercise.admin_order_field = 'exercise__name'

    def save_model(self, request, obj, form, change):
        AfterSave.save_model(self=self, request=request, obj=obj, form=form, change=change)

class FitnessAdmin(admin.ModelAdmin):
    search_fields = ['workout__appointment', 'rate']
    list_display = ['get_workout', 'appointment', 'heart_rate_average', 'updated_date', 'created_date', 'created_by', 'updated_by']
    # list_display_links = ['id', 'get_sport']
    list_filter = ('workout__appointment',)

    def get_workout(self, obj):
        return obj.workout.appointment

    get_workout.short_description = 'Workout Appointment'
    get_workout.admin_order_field = 'workout__appointment'

    def save_model(self, request, obj, form, change):
        AfterSave.save_model(self=self, request=request, obj=obj, form=form, change=change)
    # heart_rate_average = models.FloatField(blank=True, null=True, default=0)
    # heart_rate_max = models.FloatField(blank=True, null=True, default=0)
    # heart_rate_min = models.FloatField(blank=True, null=True, default=0)
    # duration = models.IntegerField(blank=True, null=True, default=0)
    # burned_calories = models.FloatField(blank=True, null=True, default=0)
    # appointment = models.DateTimeField(blank=True, null=True)


admin.site.register(Fitness, FitnessAdmin)
admin.site.register(Workout, WorkoutAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(ExerciseIcon, ExerciseIconAdmin)
admin.site.register(ExerciseImage, ExerciseImageAdmin)
admin.site.register(ExerciseRating, ExerciseRatingAdmin)
admin.site.register(ExerciseVideo, ExerciseVideoAdmin)
