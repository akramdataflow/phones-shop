from django.db import models
from autoslug import AutoSlugField


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    body = models.TextField(blank=True)

    def __str__(self):
        return self.name