from django.db import models

# Create your models here.
class search_categories(models.Model):
    image = models.ImageField(upload_to='slider_images/', blank=True, null=True)
    url = models.URLField(blank=True)
    name = models.CharField(default="",max_length=20)

    class Meta:
        verbose_name = "Search Category"
        verbose_name_plural = "Search Categories"

    def __str__(self):
      return self.name
    
class top_searches(models.Model):
    url = models.URLField(blank=True)
    name = models.CharField(default="",max_length=20)

    class Meta:
        verbose_name = "Top Search"
        verbose_name_plural = "Top Searches"

    def __str__(self):
      return self.name
    
class not_found_searches(models.Model):
    url = models.URLField(blank=True)
    name = models.CharField(default="",max_length=20)

    class Meta:
        verbose_name = "Not Found Search"
        verbose_name_plural = "Not found Searches"

    def __str__(self):
      return self.name