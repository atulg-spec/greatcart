from django.contrib import admin
from django.utils.html import format_html
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    def cat_image_tag(self, obj):
        if obj.cat_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.cat_image.url)
        return "No Image"
    cat_image_tag.short_description = 'Category Image'

    list_display = ('cat_image_tag', 'category_name', 'slug', 'description')
    prepopulated_fields = {'slug': ('category_name',)}
    search_fields = ('category_name', 'description')
    list_filter = ('category_name',)
    ordering = ('category_name',)
    fieldsets = (
        ('Category Information', {
            'fields': ('category_name', 'slug', 'description', 'cat_image')
        }),
    )

admin.site.register(Category, CategoryAdmin)
