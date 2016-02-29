from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from silent_night.mixins.models import TimeStamped, Ownable
from django.contrib.postgres.fields import jsonb


class Settings(TimeStamped, Ownable):
    """
    Stores settings in a JSON object
    """
    class Meta:
        abstract = True
        ordering = ["-created"]

    name = models.CharField(_("Name"), max_length=50, blank=True, null=True)
    data = jsonb.JSONField(_("Data"), default={})

    def get_setting(self, setting_name, default=None):
        try:
            return self.data[setting_name] or default
        except KeyError:
            return default