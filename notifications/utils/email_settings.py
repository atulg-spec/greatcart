# utils/email_settings.py
from django.conf import settings
from notifications.models import EmailSettings

def get_email_settings():
    """Get the active email settings from database or fall back to settings.py"""
    try:
        active_settings = EmailSettings.objects.filter(is_active=True).first()
        if active_settings:
            return active_settings.as_dict()
    except:
        pass  # Handle case when migrations haven't run yet
    
    # Fall back to settings.py
    return {
        'EMAIL_BACKEND': getattr(settings, 'EMAIL_BACKEND', ''),
        'EMAIL_HOST': getattr(settings, 'EMAIL_HOST', ''),
        'EMAIL_PORT': getattr(settings, 'EMAIL_PORT', 587),
        'EMAIL_USE_TLS': getattr(settings, 'EMAIL_USE_TLS', True),
        'EMAIL_HOST_USER': getattr(settings, 'EMAIL_HOST_USER', ''),
        'EMAIL_HOST_PASSWORD': getattr(settings, 'EMAIL_HOST_PASSWORD', ''),
        'DEFAULT_FROM_EMAIL': getattr(settings, 'DEFAULT_FROM_EMAIL', ''),
    }