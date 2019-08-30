from django.contrib import admin
from .models import Vacancy, UserProfile
# Register your models here.


class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'company',
                    'city']
    list_filter = ['city']


admin.site.register(Vacancy)
admin.site.register(UserProfile)