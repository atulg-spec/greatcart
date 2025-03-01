from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percentage', 'minimum_shopping_amount', 'expiry_date', 'is_active')
    list_filter = ('is_active', 'expiry_date')
    search_fields = ('code',)