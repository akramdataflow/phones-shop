import decimal

from django.db import models
from django.utils.translation import gettext_lazy as _


def image_upload(instance, filename):
    ___, extension = filename.split('.')
    return "product/%s.%s" % (instance.id, extension)


class ProductManager(models.Manager):
    def get_queryset(self):
        return (
            super(ProductManager, self).get_queryset()
            .select_related('category', 'brand', 'productvariant_set__size', 'productvariant_set__color')
            .prefetch_related('productvariant_set')
        )

class Product(models.Model):
    objects = ProductManager()
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=image_upload, null=True, blank=True)
    brand = models.ForeignKey("core.Brand", on_delete=models.CASCADE)
    category = models.ForeignKey("core.Category", on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    has_size = models.BooleanField(verbose_name=_("Product has Size"), default=False)
    has_color = models.BooleanField(verbose_name=_("Product has Color"), default=False)

    def __str__(self):
        return self.name

    def get_total_price(self, size_id: int = None) -> decimal.Decimal:
        total_price = decimal.Decimal(self.price)  # type: ignore
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
    size = models.ForeignKey("core.Size", on_delete=models.SET_NULL, null=True)
    color = models.ForeignKey("core.Color", on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=decimal.Decimal(0.0))

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.price}"

    def get_total_price(self):
        return self.price * self.quantity  # type: ignore