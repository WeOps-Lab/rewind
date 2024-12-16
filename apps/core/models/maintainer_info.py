from django.db import models
from django.utils.translation import gettext_lazy as _


class MaintainerInfo(models.Model):
    """
    Add maintainer fields to another models.
    """

    class Meta:
        verbose_name = _("Maintainer Fields")
        abstract = True

    created_by = models.CharField(_("Creator"), max_length=32, default="")
    updated_by = models.CharField(_("Updater"), max_length=32, default="")
