from django.contrib import admin
from django.utils.html import format_html
from .models import BlogSettings, Pages

@admin.register(BlogSettings)
class BlogSettingsAdmin(admin.ModelAdmin):
    list_display = ('page_title', 'banner_thumbnail', 'short_meta_description')
    readonly_fields = ('banner_preview',)
    
    fieldsets = (
        ('Banner Image', {
            'fields': ('banner_image', 'banner_preview'),
        }),
        ('SEO Metadata', {
            'fields': ('page_title', 'meta_title', 'meta_description', 'meta_keywords', 'links'),
            'description': 'Set SEO-friendly meta information for your blog.'
        }),
    )

    def banner_preview(self, obj):
        if obj.banner_image:
            return format_html('<img src="{}" style="max-height: 200px; border-radius: 10px;" />', obj.banner_image.url)
        return "No image uploaded"
    banner_preview.short_description = "Banner Preview"

    def banner_thumbnail(self, obj):
        if obj.banner_image:
            return format_html('<img src="{}" style="height: 40px; border-radius: 4px;" />', obj.banner_image.url)
        return "-"
    banner_thumbnail.short_description = "Banner"

    def short_meta_description(self, obj):
        return (obj.meta_description[:75] + '...') if len(obj.meta_description) > 75 else obj.meta_description
    short_meta_description.short_description = "Meta Description"

@admin.register(Pages)
class PagesAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'slug', 'meta_title', 'meta_keywords')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ("Basic Info", {
            'fields': ('title', 'slug', 'banner_image', 'content')
        }),
        ("SEO Settings", {
            'fields': ('page_title', 'meta_title', 'meta_description', 'meta_keywords', 'links'),
            'description': 'Fill out SEO metadata fields carefully to improve search engine visibility.'
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-updated_at')
