from django.contrib import admin
from django.utils.html import format_html
from .models import advertisement

@admin.register(advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'url')
    readonly_fields = ('image_preview',)
    search_fields = ('url',)
        
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 60px; border-radius: 4px;" />', obj.image.url)
        return "(No image)"
    image_preview.short_description = "Preview"
