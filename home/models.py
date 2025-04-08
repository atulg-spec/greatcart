from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.db import models
from django.utils.text import slugify

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=15, blank=True)
    site_header_news = CKEditor5Field('Site Header News', config_name='extends')
    slider_news = CKEditor5Field('Slider News', config_name='extends', null=True, blank=True)

    preloader_img = models.ImageField(upload_to='logos/', blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    logo_width = models.IntegerField(default=144, help_text='size in px')
    logo_height = models.IntegerField(default=72, help_text='size in px')
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

    login_banner = models.ImageField(upload_to='login/', blank=True, null=True)
    login_banner_desktop = models.ImageField(upload_to='login/', blank=True, null=True)

    product_return_details = CKEditor5Field('Product Return Details', config_name='extends', null=True, blank=True)

    gst_percentage = models.PositiveIntegerField(default=5)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

class Slider(models.Model):
    image = models.ImageField(upload_to='slider_images/', blank=True, null=True)
    url = models.URLField(blank=True)
    is_mobile = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Slider"
        verbose_name_plural = "Sliders"

    def __str__(self):
      return "Slider"
    
class featured_categories(models.Model):
    image = models.ImageField(upload_to='slider_images/', blank=True, null=True)
    name = models.CharField(max_length=50, default="")

    class Meta:
        verbose_name = "Featured Category"
        verbose_name_plural = "Featured Categories"

    def __str__(self):
      return self.name
    

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


class SideNav(models.Model):
    logo = models.ImageField(upload_to='logo/', blank=True, null=True)
    name = models.CharField(default="",max_length=50)
    url = models.URLField(blank=True)
    class Meta:
        verbose_name = "Side Navbar"
        verbose_name_plural = "Side Navbars"
    def __str__(self):
      return f"Side Nav {self.name}"


class homeSections(models.Model):
    from store.models import Product
    heading = models.CharField(default="", max_length=50)
    name = models.CharField(default="", max_length=50)
    products = models.ManyToManyField(Product)
    url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Home Section"
        verbose_name_plural = "Home Sections"
    def __str__(self):
      return f"Home Section {self.name}"


class ProductByCategory(models.Model):
    image = models.ImageField(upload_to='slider_images/', blank=True, null=True)
    url = models.URLField(blank=True)

    class Meta:
        verbose_name = "Product By Category"
        verbose_name_plural = "Product By Category"

    def __str__(self):
        return "Product By Category"
    

class Page(models.Model):
    # Page URL (slug)
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text="The URL of the page (e.g., 'about-us'). Automatically generated from the title if not provided.",
        blank=True,
    )

    # Page title
    title = models.CharField(
        max_length=200,
        help_text="The title of the page (e.g., 'About Us'). This will appear in the browser tab and as the H1 tag.",
    )

    # Meta description
    meta_description = models.CharField(
        max_length=300,
        blank=True,
        help_text="A brief description of the page for SEO purposes (160-300 characters recommended).",
    )

    # Meta keywords (less important for modern SEO, but still used by some search engines)
    meta_keywords = models.CharField(
        max_length=200,
        blank=True,
        help_text="Comma-separated keywords for SEO purposes (e.g., 'about us, company, history').",
    )

    # Page content
    content = CKEditor5Field('Content', config_name='extends')

    # Canonical URL (to avoid duplicate content issues)
    canonical_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="The canonical URL of the page (e.g., 'https://example.com/about-us').",
    )

    # Open Graph (OG) tags for social media sharing
    og_title = models.CharField(
        max_length=200,
        blank=True,
        help_text="The title of the page for social media sharing (e.g., 'About Us | Company Name').",
    )
    og_description = models.CharField(
        max_length=300,
        blank=True,
        help_text="The description of the page for social media sharing.",
    )
    og_image = models.URLField(
        max_length=500,
        blank=True,
        help_text="The URL of the image to display when the page is shared on social media.",
    )

    # Twitter Card tags for Twitter sharing
    twitter_card = models.CharField(
        max_length=50,
        blank=True,
        help_text="The type of Twitter card to use (e.g., 'summary', 'summary_large_image').",
    )
    twitter_title = models.CharField(
        max_length=200,
        blank=True,
        help_text="The title of the page for Twitter sharing.",
    )
    twitter_description = models.CharField(
        max_length=300,
        blank=True,
        help_text="The description of the page for Twitter sharing.",
    )
    twitter_image = models.URLField(
        max_length=500,
        blank=True,
        help_text="The URL of the image to display when the page is shared on Twitter.",
    )

    # Structured Data (JSON-LD for rich snippets)
    structured_data = models.TextField(
        blank=True,
        help_text="JSON-LD structured data for rich snippets (e.g., FAQ, Article, Breadcrumb).",
    )

    # Robots meta tag (to control indexing)
    robots_index = models.BooleanField(
        default=True,
        help_text="Whether search engines should index this page.",
    )
    robots_follow = models.BooleanField(
        default=True,
        help_text="Whether search engines should follow links on this page.",
    )

    # Additional fields
    is_published = models.BooleanField(
        default=True,
        help_text="Whether the page is published and visible on the site.",
    )
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
        ordering = ['title']