from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from silent_night.mixins.models import TimeStamped, Owned


class Player(TimeStamped, Owned):
    class Meta:
        verbose_name = _("Player")
        verbose_name_plural = _("Players")
        ordering = ["-created"]


