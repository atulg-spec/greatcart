from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Product, Variation, ProductGallery, ReviewRating, RecentlyStalked

# Register your models here.

class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = 'Image Preview'


class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1
    readonly_fields = ('created_date',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'image_preview', 'product_name', 'category', 'feature_category', 'price', 'discount_percent', 'before_discount_price', 'stock',
        'is_available', 'average_rating', 'review_count', 'created_date', 'modified_date', 'product_link'
    )
    list_filter = ('category', 'feature_category', 'is_available', 'created_date', 'modified_date')
    search_fields = ('product_name', 'description')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [VariationInline, ProductGalleryInline]
    readonly_fields = ('created_date', 'modified_date', 'before_discount_price', 'average_rating', 'review_count', 'image_preview')
    list_per_page = 20


    fieldsets = (
        ('Product Information', {
            'fields': ('product_name', 'slug', 'description', 'coupons', 'size_chart', 'category', 'feature_category', 'price', 'discount_percent', 'before_discount_price', 'stock', 'is_available')
        }),
        ('Images', {
            'fields': ('images', 'secondary_image', 'image_preview')
        }),
        ('Dates', {
            'fields': ('created_date', 'modified_date')
        }),
        ('SEO Information', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'product_sku', 'product_brand', 'product_mpn', 'product_gtin')
        }),
    )


    def image_preview(self, obj):
        if obj.images:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.images.url)
        return "No Image"

    image_preview.short_description = 'Product Image'

    def average_rating(self, obj):
        return f"{obj.averageReview():.1f} ⭐"

    average_rating.short_description = 'Avg Rating'

    def review_count(self, obj):
        return obj.countReview()

    review_count.short_description = 'Reviews'

    def product_link(self, obj):
        url = reverse('admin:store_product_change', args=[obj.id])
        return mark_safe(f'<a href="{url}">Edit</a>')

    product_link.short_description = 'Action'

    def save_model(self, request, obj, form, change):
        if obj.discount_percent and obj.price:
            obj.before_discount_price = int(obj.price / (1 - (obj.discount_percent / 100)))
        else:
            obj.before_discount_price = obj.price
        super().save_model(request, obj, form, change)


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created_date')
    list_filter = ('product', 'variation_category', 'is_active', 'created_date')
    search_fields = ('product__product_name', 'variation_value')
    list_editable = ('is_active',)
    readonly_fields = ('created_date',)


@admin.register(ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.image.url)
        return "No Image"

    image_preview.short_description = 'Image Preview'


@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'status', 'created_at', 'updated_at')
    list_filter = ('product', 'user', 'rating', 'status', 'created_at', 'updated_at')
    search_fields = ('product__product_name', 'user__username', 'subject', 'review')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Review Information', {
            'fields': ('product', 'user', 'subject', 'review', 'rating', 'status')
        }),
        ('Metadata', {
            'fields': ('ip', 'created_at', 'updated_at')
        }),
    )

@admin.register(RecentlyStalked)
class RecentlyStalkedAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')  # Adjust fields as necessary
    search_fields = ('user__first_name', 'product__title')  # Enable searching by user first name and product title
