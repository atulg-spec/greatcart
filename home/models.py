from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.db import models
from store.models import Product

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=15, blank=True)
    site_header_news = CKEditor5Field('Text', config_name='extends')

    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    mobile_logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    tagline = models.CharField(max_length=100, blank=True)

    main_page_image = models.ImageField(upload_to='slider_images/', blank=True, null=True)

    main_page_timer_thumbnail = models.ImageField(upload_to='slider_images/', blank=True, null=True)
    main_page_timer_heading = models.CharField(max_length=30, blank=True)
    main_page_timer_caption = models.CharField(max_length=30, blank=True)
    main_page_timer = models.CharField(max_length=30, help_text="Format: dec 25, 2024 15:00:00")
    main_page_timer_url = models.URLField(blank=True)
    main_page_timer_strap_classes = models.CharField(max_length=500, default="bg-red-500")


    instagram = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    email = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=150, blank=True)

    instagram_page = models.URLField(blank=True)
    facebook_handle = models.URLField(blank=True)
    twitter_handle = models.URLField(blank=True)
    youtube_handle = models.URLField(blank=True)
    
    font_style = models.CharField(max_length=80, default='font-sans', help_text="font-sans, font-serif, font-mono or any Custom Class")

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

class Slider(models.Model):
    image = models.ImageField(upload_to='slider_images/', blank=True, null=True)
    url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"

    def __str__(self):
      return "Slider"


class HeadSection(models.Model):
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    favicon = models.ImageField(upload_to='favicons/', blank=True, null=True)
    site_title = models.CharField(default="", max_length=120)
    meta_title = models.CharField(default="", max_length=160, help_text="SEO-friendly title")
    meta_description = models.TextField(default="", help_text="Meta description for SEO")
    meta_keywords = models.TextField(default="", help_text="Comma-separated keywords")

    links = models.TextField(help_text="Custom links for the head section")
    custom_styles = models.TextField(help_text="Additional CSS styles")

    class Meta:
        verbose_name = "Head Section"
        verbose_name_plural = "Head Section"

    def __str__(self):
        return "Custom Head Section"




class homeSections(models.Model):
    name = models.CharField(default="", max_length=50)
    products = models.ManyToManyField(Product)
    url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Home Section"
        verbose_name_plural = "Home Sections"
    def __str__(self):
      return f"Home Section {self.name}"

class PaymentGateway(models.Model):
    razorpay_key_id = models.CharField(max_length=500,default="")
    razorpay_key_secret = models.CharField(max_length=500,default="")

    class Meta:
        verbose_name = "Payment Gateway Setting"
        verbose_name_plural = "Payment Gateway"
    def __str__(self):
      return "Payment Gateway"
    

class ProductByCategory(models.Model):
    image = models.ImageField(upload_to='slider_images/', blank=True, null=True)
    url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Product By Category"
        verbose_name_plural = "Product By Category"

    def __str__(self):
        return "Product By Category"