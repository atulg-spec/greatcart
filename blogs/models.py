from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify

class BlogSettings(models.Model):
    banner_image = models.ImageField(upload_to='blog/banners/', blank=True, null=True, help_text="Upload a banner image for the blog.")
    page_title = models.CharField(
        max_length=70,
        default="",
        help_text="Page Title (Recommended: 60-70 characters)"
    )
    meta_title = models.CharField(
        max_length=70,
        default="",
        help_text="Meta Title (Recommended: 60-70 characters)"
    )
    meta_description = models.TextField(
        max_length=320,
        default="",
        help_text="Meta Description (Recommended: 150-320 characters)"
    )
    meta_keywords = models.TextField(
        default="",
        help_text="Comma-separated keywords (Avoid keyword stuffing)"
    )
    links = models.TextField(help_text="Custom links for the head section", null=True, blank=True)

    def __str__(self):
        return f"Blog Settings: {self.meta_title or 'Untitled'}"
    
    class Meta:
        verbose_name = "Blog Setting"
        verbose_name_plural = "Blogs Settings"


class Pages(models.Model):
    banner_image = models.ImageField(upload_to='blog/banners/', blank=True, null=True, help_text="Upload a banner image for the blog.")
    
    title = models.CharField(
        max_length=200,
        help_text="The title of the page (e.g., 'About Us'). This will appear in the browser tab and as the H1 tag.",
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text="The URL of the page (e.g., 'about-us'). Automatically generated from the title if not provided.",
        blank=True,
    )

    content = CKEditor5Field('Content', config_name='extends')


    page_title = models.CharField(
        max_length=70,
        default="",
        help_text="Page Title (Recommended: 60-70 characters)"
    )
    meta_title = models.CharField(
        max_length=70,
        default="",
        help_text="Meta Title (Recommended: 60-70 characters)"
    )
    meta_description = models.TextField(
        max_length=320,
        default="",
        help_text="Meta Description (Recommended: 150-320 characters)"
    )
    meta_keywords = models.TextField(
        default="",
        help_text="Comma-separated keywords (Avoid keyword stuffing)"
    )
    links = models.TextField(help_text="Custom links for the head section", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Automatically generate the slug from the title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"