import decimal
import os

from django.db import models
from django.utils.translation import gettext_lazy as _
from autoslug.fields import AutoSlugField


def image_upload(instance, filename):
    ___, extension = os.path.splitext(filename)
    return f"products/{instance.id}/images/{instance.id}{extension}"


class ProductManager(models.Manager):
    def get_queryset(self):
        return (
            super(ProductManager, self).get_queryset()
            .select_related(
                'category', 'brand', 
            )
            .prefetch_related(
                'productvariant_set', 'productimage_set',
            )
        )

class Product(models.Model):
    objects = ProductManager()
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
    
    LABELS = (
        ("new", _("New")),
        ("hot", _("Hot")),
        ("sale", _("Sale")),
        ("top", _("Top")),
        ("popular", _("Popular")),
        ("out-of-stock", _("Out of Stock")),
    )

    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)  # type: ignore
    label = models.CharField(max_length=255, choices=LABELS, null=True, blank=True)
    image = models.ImageField(upload_to=image_upload, null=True, blank=True)
    brand = models.ForeignKey("core.Brand", on_delete=models.CASCADE)
    category = models.ForeignKey("core.Category", on_delete=models.CASCADE)
    currency = models.ForeignKey("core.Currency", on_delete=models.CASCADE, default=2)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_featured = models.BooleanField(default=False)
    has_size = models.BooleanField(verbose_name=_("Product has Size"), default=False)
    has_color = models.BooleanField(verbose_name=_("Product has Color"), default=False)

    def __str__(self):
        return self.name

    def get_total_price(self, size_id: int = None) -> decimal.Decimal:
        total_price = decimal.Decimal(self.price)  # type: ignore
        if size_id:
            variant = self.productvariant_set.filter(size_id=size_id).first() # type: ignore
            if variant:
                total_price += variant.get_total_price()
        else:
            variant = self.productvariant_set.first() # type: ignore
            if variant:
                total_price += variant.get_total_price()
        return total_price


class ProductVariant(models.Model):
    class Meta:
        verbose_name = _("Product Variant")
        verbose_name_plural = _("Product Variants")

    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    size = models.ForeignKey("core.Size", on_delete=models.SET_NULL, null=True)
    color = models.ForeignKey("core.Color", on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=decimal.Decimal(0.0))

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.price}"

    def get_total_price(self):
        return self.price * self.quantity  # type: ignore


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=image_upload,
        verbose_name=_("Product Image")
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Display Order")
    )
    
    class Meta:
        ordering = ['order']
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return f"Image for {self.product.name}"
