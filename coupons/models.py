from django.db import models
from django.utils import timezone

class Coupon(models.Model):
    # Expiry date of the coupon
    expiry_date = models.DateTimeField()

    # Discount percentage (e.g., 10 for 10%)
    discount_percentage = models.DecimalField(
        max_digits=5,  # Maximum digits (including decimal places)
        decimal_places=2,  # Decimal places
        help_text="Discount percentage (e.g., 10 for 10%)"
    )

    # Minimum shopping amount required to use the coupon
    minimum_shopping_amount = models.DecimalField(
        max_digits=10,  # Maximum digits (including decimal places)
        decimal_places=2,  # Decimal places
        help_text="Minimum shopping amount required to use the coupon"
    )

    # Optional: Add a code field for the coupon
    code = models.CharField(
        max_length=50,
        unique=True,
        help_text="Coupon code (e.g., WELCOME10)"
    )

    # Optional: Add a boolean field to check if the coupon is active
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Coupon {self.code} - {self.discount_percentage}% off"

    # Optional: Add a method to check if the coupon is expired
    def is_expired(self):
        return timezone.now() > self.expiry_date

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"