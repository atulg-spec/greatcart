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
    list_display = ("name",)
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

    list_display = ('site_name', 'logo_tag', 'mobile_logo_tag',)

    fieldsets = (
        ('Main Settings', {
            'fields': ('site_name', 'site_header_news', 'preloader_img','logo', 'mobile_logo', 'tagline', 'font_style')
        }),
        ('Index Page Banner', {
            'fields': ('main_page_image',)
        }),
        ('Index Page Timer', {
            'fields': ('main_page_timer_thumbnail', 'main_page_timer_heading', 'main_page_timer_caption','main_page_timer','main_page_timer_url', 'main_page_timer_strap_classes')
        }),
        ('Contact Info', {
            'fields': ('instagram', 'phone_number', 'email', 'location')
        }),
        ('Social Media', {
            'fields': ('instagram_page', 'facebook_handle', 'twitter_handle', 'youtube_handle')
        }),
        ('Login/SignUp', {
            'fields': ('login_banner', 'login_banner_desktop')
        }),
    )

    def has_add_permission(self, request):
        # Allows addition only if no instance exists
        return not SiteSettings.objects.exists()

    def logo_tag(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.logo.url)
        return "No Logo"

    def mobile_logo_tag(self, obj):
        if obj.mobile_logo:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.mobile_logo.url)
        return "No Mobile Logo"

    # Short descriptions for each image tag
    logo_tag.short_description = 'Logo'
    mobile_logo_tag.short_description = 'Mobile Logo'



class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = ('razorpay_key_id', 'razorpay_key_secret')
    search_fields = ('razorpay_key_id',)

    def has_add_permission(self, request):
        # Restrict adding more than one PaymentGateway object
        if PaymentGateway.objects.exists():
            return False
        return super().has_add_permission(request)

admin.site.register(PaymentGateway, PaymentGatewayAdmin)

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
    list_display = ('title', 'slug', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('title', 'slug', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'content', 'is_published'),
        }),
        ('SEO Metadata', {
            'fields': ('meta_description', 'meta_keywords', 'canonical_url'),
        }),
        ('Open Graph (Social Media)', {
            'fields': ('og_title', 'og_description', 'og_image'),
        }),
        ('Twitter Card', {
            'fields': ('twitter_card', 'twitter_title', 'twitter_description', 'twitter_image'),
        }),
        ('Structured Data', {
            'fields': ('structured_data',),
        }),
        ('Robots Meta Tag', {
            'fields': ('robots_index', 'robots_follow'),
        }),
    )
