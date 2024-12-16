from django.db import models
from django.db.models import (
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    Field,
    FloatField,
    IntegerField,
    JSONField,
    TimeField,
)
from django.utils.translation import gettext_lazy as _


class VtypeMixin(models.Model):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    DATETIME = "datetime"
    TIME = "time"
    DATE = "date"
    JSON = "json"
    BOOLEAN = "bool"
    DEFAULT = "default"

    VTYPE_FIELD_MAPPING = {
        STRING: CharField,
        INTEGER: IntegerField,
        FLOAT: FloatField,
        DATETIME: DateTimeField,
        DATE: DateField,
        TIME: TimeField,
        JSON: JSONField,
        BOOLEAN: BooleanField,
        DEFAULT: Field,
    }
    VTYPE_CHOICE = (
        (STRING, _("string")),
        (INTEGER, _("integer")),
        (FLOAT, _("float")),
        (DATETIME, _("datetime")),
        (TIME, _("time")),
        (DATE, _("date")),
        (JSON, _("json")),
        (BOOLEAN, _("boolean")),
        (DEFAULT, _("default")),
    )

    vtype = models.CharField(_("Type"), max_length=32, default=STRING)

    class Meta:
        verbose_name = _("Text Value Type Fields")
        abstract = True
