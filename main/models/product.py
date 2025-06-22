import decimal
import os
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from autoslug.fields import AutoSlugField


def image_upload(instance, filename):
    ___, extension = os.path.splitext(filename)
    return f"products/{instance.id}/images/{uuid.uuid4().hex}{extension}"


class ProductManager(models.Manager):
    def get_queryset(self):
        return (
            super(ProductManager, self).get_queryset()
            .select_related(
                'category', 'brand', 'currency'
            )
            .prefetch_related(
                'productvariant_set__color', 'productvariant_set__size', 'productimage_set',
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

    # --- Translation Fields Added ---
    name = models.CharField(_("Product Name (English)"), max_length=255)
    name_ar = models.CharField(_("Product Name (Arabic)"), max_length=255, blank=True, null=True)
    description = models.TextField(_("Description (English)"))
    description_ar = models.TextField(_("Description (Arabic)"), blank=True, null=True)
    # --- End of Translation Fields ---

    slug = AutoSlugField(populate_from='name', unique=True)  # type: ignore
    label = models.CharField(max_length=255, choices=LABELS, null=True, blank=True)
    image = models.ImageField(upload_to=image_upload, null=True, blank=True)
    brand = models.ForeignKey("core.Brand", on_delete=models.CASCADE, verbose_name=_("Brand"))
    category = models.ForeignKey("core.Category", on_delete=models.CASCADE, verbose_name=_("Category"))
    currency = models.ForeignKey("core.Currency", on_delete=models.CASCADE, default=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_featured = models.BooleanField(default=False)
    has_size = models.BooleanField(verbose_name=_("Product has Size Variants"), default=False)
    has_color = models.BooleanField(verbose_name=_("Product has Color Variants"), default=False)

    def __str__(self):
        return self.name

    def get_total_price(self, size_id: int = None) -> decimal.Decimal:
        total_price = decimal.Decimal(self.price)
        if size_id:
            variant = self.productvariant_set.filter(size_id=size_id).first()
            if variant:
                total_price += variant.get_total_price()
        else:
            variant = self.productvariant_set.first()
            if variant:
                total_price += variant.get_total_price()
        return total_price


class ProductVariant(models.Model):
    class Meta:
        verbose_name = _("Product Variant")
        verbose_name_plural = _("Product Variants")

    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    size = models.ForeignKey("core.Size", on_delete=models.SET_NULL, null=True, blank=True)
    color = models.ForeignKey("core.Color", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(_("Quantity"), default=1, help_text=_("Set to 0 if out of stock"))
    price = models.DecimalField(max_digits=10, decimal_places=2, default=decimal.Decimal(0.0), help_text=_("Additional price for this variant, can be 0"))

    def __str__(self):
        parts = [self.product.name]
        if self.color:
            parts.append(self.color.name)
        if self.size:
            parts.append(self.size.name)
        return " - ".join(parts)

    def get_total_price(self):
        return self.price * self.quantity


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