# models.py
from django.db import models
from django.core.exceptions import ValidationError

class EmailSettings(models.Model):
    EMAIL_BACKEND_CHOICES = [
        ('smtp', 'SMTP'),
        ('console', 'Console (for testing)'),
        ('file', 'File (for testing)'),
    ]
    
    email_backend = models.CharField(
        max_length=50,
        choices=EMAIL_BACKEND_CHOICES,
        default='smtp',
        help_text="Backend to use for sending emails"
    )
    email_host = models.CharField(
        max_length=255,
        default='smtp.gmail.com',
        help_text="SMTP server address"
    )
    email_port = models.PositiveIntegerField(
        default=587,
        help_text="SMTP server port"
    )
    email_use_tls = models.BooleanField(
        default=True,
        help_text="Whether to use TLS (secure) connection"
    )
    email_host_user = models.EmailField(
        max_length=255,
        help_text="Email address used to send emails"
    )
    email_host_password = models.CharField(
        max_length=255,
        blank=True,
        help_text="Password for the email account"
    )
    default_from_email = models.EmailField(
        max_length=255,
        help_text="Default 'from' address for emails"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether these settings are active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Email Settings"
        verbose_name_plural = "Email Settings"
        ordering = ['-is_active', '-updated_at']

    def __str__(self):
        return f"Email Settings (Active: {self.is_active})"

    def clean(self):
        if self.is_active:
            # Ensure only one active configuration exists
            active_configs = EmailSettings.objects.filter(is_active=True)
            if self.pk:
                active_configs = active_configs.exclude(pk=self.pk)
            if active_configs.exists():
                raise ValidationError(
                    "Only one active email configuration is allowed. "
                    "Please deactivate the other configuration first."
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def as_dict(self):
        """Return settings as a dictionary compatible with Django's email settings"""
        return {
            'EMAIL_BACKEND': self.get_backend_path(),
            'EMAIL_HOST': self.email_host,
            'EMAIL_PORT': self.email_port,
            'EMAIL_USE_TLS': self.email_use_tls,
            'EMAIL_HOST_USER': self.email_host_user,
            'EMAIL_HOST_PASSWORD': self.email_host_password,
            'DEFAULT_FROM_EMAIL': self.default_from_email,
        }

    def get_backend_path(self):
        """Get the full backend path based on the selected choice"""
        backends = {
            'smtp': 'django.core.mail.backends.smtp.EmailBackend',
            'console': 'django.core.mail.backends.console.EmailBackend',
            'file': 'django.core.mail.backends.filebased.EmailBackend',
        }
        return backends.get(self.email_backend, backends['smtp'])
    

class SiteNotifications(models.Model):
    banner_image = models.ImageField(upload_to='photos/siteads',null=True,blank=True)
    url = models.URLField()

    def __str__(self):
        return 'Site Notifications Banner'
    
    class Meta:
        verbose_name = "Site Notification"
        verbose_name_plural = "Site Notifications"
