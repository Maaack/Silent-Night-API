import numpy
import pymunk
import random
import math
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

    def __init__(self, settings, seed=None):
        if type(settings) is not SpaceSettings:
            raise TypeError
        super(Space, self).__init__()
        self.settings = settings
        self.space_width = self.get_settings('space_width', 100.0)
        self.space_depth = self.get_settings('space_depth', 100.0)
        self.space_max_x = self.space_width/2
        self.space_min_x = -self.space_max_x
        self.space_max_y = self.space_depth/2
        self.space_min_y = -self.space_max_y

        self.start_space(seed)
        self.bodies = {}

    @staticmethod
    def new_seed():
        string = "0123456789abcdef"
        seed = ""
        for i in range(0, 20):
            pos = random.randrange(0, len(string)-1)
            seed += string[pos]
        return seed
    
    def get_setting(self, setting_name, default=None):
        return self.settings.data[setting_name] or default

    def start_space(self, seed=None):
        self.seed = seed or Space.new_seed()
        random.seed(self.seed)
        self.game_space = pymunk.Space()

    def populate_space(self):
        self.populate_asteroids()

    def populate_asteroids(self):
        asteroid_count = self.get_setting('asteroid_count', 100)
        asteroid_mass_min = self.get_settings('asteroid_mass_min', 1.0)
        asteroid_mass_max = self.get_settings('asteroid_mass_max', 100.0)
        asteroid_radius_min = self.get_settings('asteroid_radius_min', 10.0)
        asteroid_radius_max = self.get_settings('asteroid_radius_max', 50.0)
        asteroid_velocity_min = self.get_settings('asteroid_velocity_min', 0.0)
        asteroid_velocity_max = self.get_settings('asteroid_velocity_max', 30.0)

        for i in range(0, asteroid_count):
            from .classes import Asteroid
            mass = random.randrange(asteroid_mass_min, asteroid_mass_max)
            radius = random.randrange(asteroid_radius_min, asteroid_radius_max)
            position = self.get_random_position()
            velocity = Space.get_random_velocity(asteroid_velocity_min, asteroid_velocity_max)
            asteroid = Asteroid(self, radius, mass, position, velocity)
            self.bodies[asteroid['id']] = asteroid

    def get_random_position(self):
        return (random.randrange(self.space_min_x, self.space_max_x),
                random.randrange(self.space_min_y, self.space_max_y))

    @staticmethod
    def get_random_velocity(min_velocity, max_velocity):
        new_angle = random.uniform(0, math.pi*2)
        new_x = math.sin(new_angle)
        new_y = math.cos(new_angle)
        new_vector = numpy.array([new_x, new_y])
        new_vector.linalg.normalize()
        new_vector *= random.randrange(min_velocity, max_velocity)
        return new_vector


class SpaceSettings(Settings):
    class Meta:
        verbose_name = _("Space Settings")
        verbose_name_plural = _("Space Settings")
