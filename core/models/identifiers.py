from django.utils.translation import gettext_lazy as _
from django.db import models
from uuid import uuid4


class UniqueIdentifierModel(models.Model):
    guid = models.UUIDField(
        unique=True, default=uuid4, editable=False, verbose_name=_("Unique ID"),
        help_text=_("This field is automatically determined by the system, do not interfere.")
    )

    class Meta:
        abstract = True

    def get_dict(self):
        return {
            "guid": str(self.guid),
        }

    def get_uid(self):
        return str(self.guid)


class Tokenizer(UniqueIdentifierModel):
    class Meta:
        verbose_name = _("Tokenizer")
        verbose_name_plural = verbose_name

    uidb64 = models.CharField(max_length=255)
    token = models.CharField(max_length=255)

    def __str__(self):
        return str(self.guid)