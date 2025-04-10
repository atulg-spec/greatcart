from django.contrib import admin
from .models import *
from django_ckeditor_5.widgets import CKEditor5Widget
from django.forms import ModelForm
from django.utils.html import format_html

# Custom form to use CKEditor5 widget in the admin
class SiteSettingsForm(ModelForm):
    class Meta:
        model = SiteSettings
        fields = '__all__'
        widgets = {
            'site_header_news': CKEditor5Widget(config_name='extends'),
        }

@admin.register(homeSections)
class HomeSectionsAdmin(admin.ModelAdmin):
    filter_horizontal = ('products',)
    list_display = ("name", 'heading')
    search_fields = ("name",)
    list_per_page = 20
    ordering = ("id",)
    
    def has_add_permission(self, request):
        return True  # Change to False if you want to prevent adding new entries
    
    def has_delete_permission(self, request, obj=None):
        return True  # Change to False if you want to prevent deletion

@admin.register(SideNav)
class SideNavAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')  # Fields to display in the list view
    search_fields = ('name',)  # Fields to search by in the admin
    list_filter = ('name',)  # Fields to filter by in the admin
    ordering = ('name',)  # Default ordering of the list view

    # Optional: Customize the form in the admin
    fieldsets = (
        (None, {
            'fields': ('logo', 'name', 'url')
        }),
    )

@admin.register(HeadSection)
class HeadSectionAdmin(admin.ModelAdmin):
    list_display = ('preview_logo', 'preview_favicon', 'site_title', 'meta_title')
    readonly_fields = ('preview_logo', 'preview_favicon')
    fieldsets = (
        ('General Settings', {
            'fields': ('logo', 'preview_logo', 'favicon', 'preview_favicon', 'site_title')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        ('Customization', {
            'fields': ('links', 'custom_styles')
        }),
    )

    def preview_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:5px;"/>', obj.logo.url)
        return "No Logo"
    preview_logo.short_description = "Logo Preview"

    def preview_favicon(self, obj):
        if obj.favicon:
            return format_html('<img src="{}" width="20" height="20" style="border-radius:3px;"/>', obj.favicon.url)
        return "No Favicon"
    preview_favicon.short_description = "Favicon Preview"

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    form = SiteSettingsForm

    list_display = ('site_name', 'logo_tag')

    fieldsets = (
        ('Main Settings', {
            'fields': ('site_name', 'site_header_news', 'slider_news', 'preloader_img','logo', 'logo_width', 'logo_height', 'tagline', 'font_style')
        }),
        ('Index Page Banner', {
            'fields': ('main_page_image', 'main_page_image_url')
        }),
        ('Index Page Timer', {
            'fields': ('main_page_timer_thumbnail', 'main_page_timer_heading', 'main_page_timer_caption','main_page_timer','main_page_timer_url', 'main_page_timer_strap_classes')
        }),
        ('Contact Info', {
            'fields': ('phone_number', 'email', 'location')
        }),
        ('Social Media', {
            'fields': ('instagram_handle', 'facebook_handle', 'twitter_handle', 'youtube_handle')
        }),
        ('Login/SignUp', {
            'fields': ('login_banner', 'login_banner_desktop')
        }),
        ('Product Return Description', {
            'fields': ('product_return_details',)
        }),
        ('Financial Details', {
            'fields': ('gst_percentage',)
        }),
    )

    def has_add_permission(self, request):
        # Allows addition only if no instance exists
        return not SiteSettings.objects.exists()

    def logo_tag(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.logo.url)
        return "No Logo"


    # Short descriptions for each image tag
    logo_tag.short_description = 'Logo'


@admin.register(featured_categories)
class FeaturedCategoriesAdmin(admin.ModelAdmin):
    list_display = ('display_image', 'name')
    readonly_fields = ('image_preview',)
    list_display_links = ('display_image',)
    
    fieldsets = (
        (None, {
            'fields': ('image', 'image_preview', 'name')
        }),
    )
    
    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;" />',
                obj.image.url
            )
        return "-"
    display_image.short_description = 'Image Preview'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 300px; max-width: 100%;" />',
                obj.image.url
            )
        return "No image uploaded yet."
    image_preview.short_description = 'Large Preview'    



class ProductByCategoryAdmin(admin.ModelAdmin):
    list_display = ('display_image', 'url')  # Include the display_image method
    search_fields = ('url',)
    list_filter = ('image',)
    ordering = ('url',)

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'  # Column header name in the admin

# Register the model with the admin interface
admin.site.register(ProductByCategory, ProductByCategoryAdmin)


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'url', 'is_mobile')
    search_fields = ('url',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border-radius:5px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Preview"


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at')
    search_fields = ('title', 'slug', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'content', 'links'),
        }),
        ('SEO Metadata', {
            'fields': ('meta_description', 'meta_keywords'),
        }),
        ('Open Graph (Social Media)', {
            'fields': ('og_title', 'og_description'),
        }),
        ('Structured Data', {
            'fields': ('structured_data',),
        }),
    )
