from django.contrib import admin
from django.utils.html import format_html
from .models import search_categories, top_searches, not_found_searches

@admin.register(search_categories)
class SearchCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'image_preview')
    search_fields = ('name', 'url')
    list_filter = ('name',)
    fieldsets = (
        (None, {
            'fields': ('image', 'url', 'name')
        }),
    )
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:5px;" />', obj.image.url)
        return "-"
    image_preview.short_description = "Image Preview"

@admin.register(top_searches)
class TopSearchAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name', 'url')
    list_filter = ('name',)

@admin.register(not_found_searches)
class NotFoundSearchAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name', 'url')
    list_filter = ('name',)
