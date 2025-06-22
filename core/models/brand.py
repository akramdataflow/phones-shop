from django.db import models
from django.utils.translation import gettext_lazy as _
from autoslug.fields import AutoSlugField

class Brand(models.Model):
    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')

    # The original name field, can be used for English
    name = models.CharField(
        _("Brand Name (English)"), 
        max_length=100, 
        unique=True
    )
    
    # The new field for the Arabic name
    name_ar = models.CharField(
        _("Brand Name (Arabic)"), 
        max_length=100, 
        blank=True, 
        null=True
    )

    # Slug will be generated from the primary name field
    slug = AutoSlugField(populate_from='name', unique=True)  # type: ignore
    
    # Optional: You can also add a translated body/description if needed
    body = models.TextField(
        _("Description"), 
        blank=True
    )
    
    image = models.ImageField(
        _("Brand Image"), 
        upload_to='brands', 
        null=True, 
        blank=True
    )

    def __str__(self):
        return self.name