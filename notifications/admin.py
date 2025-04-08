from django.utils.html import format_html
from django.contrib import admin
from .models import EmailSettings, SiteNotifications

@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    list_display = ('email_host_user', 'email_host', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    fieldsets = (
        ('Status', {
            'fields': ('is_active',)
        }),
        ('SMTP Configuration', {
            'fields': (
                'email_backend',
                'email_host',
                'email_port',
                'email_use_tls',
            )
        }),
        ('Authentication', {
            'fields': (
                'email_host_user',
                'email_host_password',
                'default_from_email',
            )
        }),
    )


@admin.register(SiteNotifications)
class SiteNotificationsAdmin(admin.ModelAdmin):
    list_display = ('banner_preview', 'url')
    readonly_fields = ('banner_preview',)

    def banner_preview(self, obj):
        if obj.banner_image:
            return format_html(
                '<img src="{}" style="max-height: 120px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.15);" />',
                obj.banner_image.url
            )
        return "No Image"

    banner_preview.short_description = 'Banner Preview'
