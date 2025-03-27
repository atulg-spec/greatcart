from django.contrib import admin
from django.utils.html import format_html
from .models import top_searches, not_found_searches

@admin.register(top_searches)
class TopSearchAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(not_found_searches)
class NotFoundSearchAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
