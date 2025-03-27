from django.db import models
    
class top_searches(models.Model):
    name = models.CharField(default="",max_length=20)

    class Meta:
        verbose_name = "Top Search"
        verbose_name_plural = "Top Searches"

    def __str__(self):
      return self.name
    
class not_found_searches(models.Model):
    name = models.CharField(default="",max_length=20)

    class Meta:
        verbose_name = "Not Found Search"
        verbose_name_plural = "Not found Searches"

    def __str__(self):
      return self.name