from django.utils.translation import gettext_lazy as _
from django.db import models
from autoslug import AutoSlugField


class Category(models.Model):
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)  # type: ignore
    body = models.TextField(blank=True)

    def __str__(self):
        return self.name