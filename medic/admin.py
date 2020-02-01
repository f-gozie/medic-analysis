from django.contrib import admin
from medic.models import UserProfile, Analysis, Ailment

class AnalysisAdmin(admin.ModelAdmin):
	list_display = ['user', 'blood_group', 'height', 'weight', 'gender', 'get_ailments']

admin.site.register(UserProfile)
admin.site.register(Analysis, AnalysisAdmin)
admin.site.register(Ailment)