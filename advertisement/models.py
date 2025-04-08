from django.db import models
from store.models import Product

class advertisement(models.Model):
    image = models.ImageField(upload_to='photos/ads', null=True, blank=True)
    url = models.URLField()

    def __str__(self):
        return 'ads'