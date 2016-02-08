from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from silent_night.mixins.models import TimeStamped, Owned
from django.contrib.postgres.fields import jsonb


class Player(TimeStamped, Owned):
    class Meta:
        verbose_name = _("Player")
        verbose_name_plural = _("Players")
        ordering = ["-created"]


class Game(TimeStamped):
    class Meta:
        verbose_name = _("Game")
        verbose_name_plural = _("Games")
        ordering = ["-created"]

    code = models.CharField(_("Code"), max_length=8)
    name = models.CharField(_("Name"), max_length=50)
    settings = models.ForeignKey("GameSettings")

    def __str__(self):
        return self.name + " | " + self.code


class GameSettings(TimeStamped):
    class Meta:
        verbose_name = _("Game Settings")
        verbose_name_plural = _("Game Settings")
        ordering = ["-created"]

    data = jsonb.JSONField(default={})
