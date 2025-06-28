from django.db import models
from django.utils.translation import gettext_lazy as _
from autoslug.fields import AutoSlugField

class Category(models.Model):
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    # The primary name field, used for English
    name = models.CharField(
        _("Category Name (English)"),
        max_length=100, 
        unique=True
    )

    # The new field for the Arabic name
    name_ar = models.CharField(
        _("Category Name (Arabic)"),
        max_length=100,
        blank=True,
        null=True
    )

    # Slug will be generated from the primary (English) name field
    slug = AutoSlugField(populate_from='name', unique=True)  # type: ignore

    body = models.TextField(
        _("Description"),
        blank=True
    )

    def __str__(self):
        return self.name