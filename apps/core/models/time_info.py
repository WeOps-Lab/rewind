from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeInfo(models.Model):
    """
    Add time fields to another models.
    """

    class Meta:
        verbose_name = _("Time Fields")
        abstract = True

    created_at = models.DateTimeField(_("Created Time"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("Updated Time"), auto_now=True)
