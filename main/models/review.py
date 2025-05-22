from django.db import models
from django.conf import settings

from core.models import TimeStampedModel


class Review(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_reviews')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')

    body = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        unique_together = ('user', 'product')
        ordering = ['-created']

    def __str__(self):
        return self.body
    
    def masked_user_email(self):
        return f"{self.user.email[:2]}...{self.user.email[-2:]}"