from django.db import models
from django.utils.translation import gettext_lazy as _


class Size(models.Model):
    class Meta:
        verbose_name = _('Size')
        verbose_name_plural = _('Sizes')

    UNITS = (
        ('kg', _('Kilograms')),
        ('g', _('Grams')),
        ('l', _('Liters')),
        ('m', _('Meters')),
        ('cm', _('Centimeters')),
        ('in', _('Inches')),
    )
    unit = models.CharField(max_length=5, choices=UNITS)
    size = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.size} {self.get_unit_display()}'  # type: ignore