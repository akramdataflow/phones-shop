from django.db import models
from autoslug import AutoSlugField


class Brand(models.Model):
    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    body = models.TextField(blank=True)

    def __str__(self):
        return self.name