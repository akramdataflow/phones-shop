# -*- encoding: utf-8 -*-
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone
from django.utils.timesince import timesince


class TimeStampedModel(models.Model):
    """
    Abstract base class that provides self-updating 'created' and 'modified' fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    ORDER_BY = (
        ("created", _("Created Ascendant"),),
        ("-created", _("Created Descendant"),),
        ("modified", _("Modified Ascendant"),),
        ("-modified", _("Modified Descendant"),),
    )
    ORDER_BY_MODIFIED_DEFAULT = "-modified"
    ORDER_BY_CREATED_DEFAULT = "-created"

    class Meta:
        abstract = True

    def get_dict(self):
        from core.utils import readable_date_format
        return {
            "created": timezone.localtime(self.created).isoformat() if self.created else None,
            "createdf": readable_date_format(timezone.localtime(self.created)) if self.created else None,
            "createds": timesince(self.created) if self.created else None,
            "modified": timezone.localtime(self.modified).isoformat() if self.modified else None,
            "modifiedf": readable_date_format(timezone.localtime(self.modified)) if self.modified else None,
            "modifieds": timesince(self.modified) if self.modified else None,
            "isedited": self.isedited,
        }

    @property
    def isedited(self):
        return False if self.created.strftime('%Y-%m-%d %H:%M:%S') == self.modified.strftime(
            '%Y-%m-%d %H:%M:%S') else True