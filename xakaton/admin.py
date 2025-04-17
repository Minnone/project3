from django.contrib import admin
from .models import Hackathon

@admin.register(Hackathon)
class HackathonAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'format', 'prize_fund', 'is_active')
    list_filter = ('is_active', 'format')
    search_fields = ('title', 'description')
    ordering = ('-start_date',)