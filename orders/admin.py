from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Payment, Order, OrderProduct, PaymentGateway

# Register your models here.
@admin.register(PaymentGateway)
class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = ('use', 'mode', 'razorpay_id', 'payu_marchent_key')
    list_filter = ('use', 'mode')
    search_fields = ('use', 'mode', 'razorpay_id', 'payu_marchent_key')
    fieldsets = (
        ('General Information', {
            'fields': ('use', 'mode'),
            'description': "Basic information about the payment gateway settings."
        }),
        ('Razorpay Configuration', {
            'fields': ('razorpay_id', 'razorpay_secret'),
            'description': "Configuration details for Razorpay payment gateway."
        }),
        ('PayU Configuration', {
            'fields': ('payu_marchent_key', 'payu_marchent_salt'),
            'description': "Configuration details for PayU payment gateway."
        }),
        ('Manual Payment QR', {
            'fields': ('qr_image', 'contact_url'),
            'description': "Configuration details for UPI QR Payments."
        }),
    )

    def has_add_permission(self, request):
        # Allow only one instance of PaymentGateway
        if PaymentGateway.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the PaymentGateway instance
        return False

    def get_actions(self, request):
        # Remove the delete action from the admin interface
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'payment_method', 'amount_paid', 'status', 'created_at')
    list_filter = ('payment_method', 'status', 'created_at')
    search_fields = ('payment_id', 'user__email', 'user__username')
    readonly_fields = ('created_at',)
    list_per_page = 20

    fieldsets = (
        ('Payment Information', {
            'fields': ('user', 'payment_id', 'payment_method', 'amount_paid', 'status')
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ('product', 'variations', 'quantity', 'product_price', 'created_at', 'updated_at', 'product_image')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def product_image(self, obj):
        if obj.product.images:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.product.images.url)
        return "No Image"

    product_image.short_description = 'Product Image'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'full_name', 'phone', 'email', 'order_total', 'tax', 'status', 'is_ordered', 'created_at', 'order_actions'
    )
    list_filter = ('status', 'is_ordered', 'created_at', 'country', 'state', 'city')
    search_fields = ('order_number', 'first_name', 'last_name', 'phone', 'email', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'order_number', 'full_name', 'full_address')
    inlines = [OrderProductInline]
    list_per_page = 20

    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'payment', 'order_number', 'status', 'is_ordered')
        }),
        ('Customer Details', {
            'fields': ('first_name', 'last_name', 'phone', 'email', 'full_name')
        }),
        ('Shipping Address', {
            'fields': ('address_line_1', 'address_line_2', 'country', 'state', 'city', 'zip_code', 'full_address')
        }),
        ('Order Details', {
            'fields': ('order_note', 'order_total', 'tax')
        }),
        ('Metadata', {
            'fields': ('ip', 'created_at', 'updated_at')
        }),
    )

    def full_name(self, obj):
        return obj.full_name()

    full_name.short_description = 'Full Name'

    def full_address(self, obj):
        return obj.full_address()

    full_address.short_description = 'Full Address'

    def order_actions(self, obj):
        url = reverse('admin:orders_order_change', args=[obj.id])
        return mark_safe(f'<a href="{url}">Edit</a>')

    order_actions.short_description = 'Actions'


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_image', 'order', 'product', 'user', 'quantity', 'product_price', 'ordered', 'created_at', 'updated_at'
    )
    list_filter = ('ordered', 'created_at', 'updated_at')
    search_fields = ('order__order_number', 'product__product_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at', 'product_image')
    list_per_page = 20

    fieldsets = (
        ('Order Product Information', {
            'fields': ('order', 'payment', 'user', 'product', 'variations', 'quantity', 'product_price', 'ordered')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def product_image(self, obj):
        if obj.product.images:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.product.images.url)
        return "No Image"

    product_image.short_description = 'Product Image'