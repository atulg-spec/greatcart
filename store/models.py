from django.db import models
from category.models import Category
from django.urls import reverse
from django.db.models import Avg, Count
from accounts.models import CustomUser
from django_ckeditor_5.fields import CKEditor5Field
from coupons.models import Coupon
# Create your models here.

class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = CKEditor5Field('Text', config_name='extends')
    coupons         = models.ManyToManyField(Coupon, blank=True)
    meta_keywords   = models.CharField(max_length=400, default="", help_text="Comma(,) Seperated Keywords")
    price           = models.IntegerField()
    size_chart      = models.ImageField(upload_to='photos/products',null=True,blank=True)
    images          = models.ImageField(upload_to='photos/products')
    secondary_image = models.ImageField(upload_to='photos/products',null=True,blank=True)
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)
    before_discount_price = models.IntegerField(default=0)
    discount_percent = models.IntegerField(default=10)

    def save(self, *args, **kwargs):
        if self.discount_percent and self.price:
            self.before_discount_price = int(self.price / (1 - (self.discount_percent / 100)))
        else:
            self.before_discount_price = self.price
        super().save(*args, **kwargs)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.product_name

    def get_colors(self):
        """Returns a QuerySet of all unique active colors for this product."""
        return self.variation_set.filter(variation_category='color', is_active=True).values_list('variation_value', flat=True).distinct()

    def get_sizes(self):
        """Returns a QuerySet of all unique active sizes for this product."""
        return self.variation_set.filter(variation_category='size', is_active=True).values_list('variation_value', flat=True).distinct()

    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count



class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value     = models.CharField(max_length=100)
    is_active           = models.BooleanField(default=True)
    created_date        = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class RecentlyStalked(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')  # Ensure unique user-product pairs

    def __str__(self):
        return f"{self.user.first_name} recently watched {self.product.product_name}"

    def save(self, *args, **kwargs):
        # Check if the user has already stalked this product
        if RecentlyStalked.objects.filter(user=self.user, product=self.product).exists():
            pass
        else:
            # Check how many RecentlyStalked objects exist for this user
            user_stalked_count = RecentlyStalked.objects.filter(user=self.user).count()
            # If the user has 10 stalked products, delete the oldest one
            if user_stalked_count >= 10:
                # Get the oldest RecentlyStalked object for this user
                oldest_stalked = RecentlyStalked.objects.filter(user=self.user).order_by('id').first()
                if oldest_stalked:
                    oldest_stalked.delete()

        # Call the original save method to save the new RecentlyStalked object
            super().save(*args, **kwargs)