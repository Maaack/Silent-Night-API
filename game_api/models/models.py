from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _

from silent_night.mixins.models import TimeStamped, Owned, Ownable
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


class Settings(TimeStamped, Ownable):
    class Meta:
        abstract = True
        ordering = ["-created"]

    name = models.CharField(_("Name"), max_length=50, blank=True, null=True)
    data = jsonb.JSONField(_("Data"), default={})


class GameSettings(Settings):
    class Meta:
        verbose_name = _("Game Settings")
        verbose_name_plural = _("Game Settings")


class Snapshot(TimeStamped):
    state = jsonb.JSONField(_("Game State"), default={})
    game_time = models.FloatField(_("Game Time in Seconds"), default=0.0)


class Space(TimeStamped):
    class Meta:
        verbose_name = _("Space")
        verbose_name_plural = _("Spaces")
        ordering = ["-created"]

    game = models.ForeignKey("Game")
    initial_snapshot = models.ForeignKey("Snapshot")
    settings = models.ForeignKey("SpaceSettings")
    seed = models.CharField(_("Random Seed"), max_length=50)


class SpaceSettings(Settings):
    class Meta:
        verbose_name = _("Space Settings")
        verbose_name_plural = _("Space Settings")
