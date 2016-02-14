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

    def __init__(self, name=None, settings=None):
        super(Game, self).__init__()
        self.space = None
        self.name = name or 'New Game'
        self.settings = settings or DefaultGameSettings.objects.first()
        self.space_settings = SpaceSettings.objects.get(id=settings.get_setting('space_settings_id'))
        # Eventually create the space

    def create_space(self):
        self.space = Space(self, self.settings['space_settings'])


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
        return self.data[setting_name] or default


class GameSettings(Settings):
    """
    Stores game settings specifically
    Example:
    JSON
    {
        "asteroid_count": 200,
        "asteroid_mass_min": 20.0,
        "asteroid_mass_max": 200.0,
        ...
    }
    """
    class Meta:
        verbose_name = _("Game Settings")
        verbose_name_plural = _("Game Settings")


class DefaultGameSettings(GameSettings):
    class Meta:
        verbose_name = _("Default Game Settings")
        verbose_name_plural = _("Default Game Settings")


class SpaceSettings(Settings):
    """
    Stores space settings specifically
    Example:
    JSON
    {
        "space_width": 1500.0,
        "space_depth": 1500.0,
        ...
    }
    """
    class Meta:
        verbose_name = _("Space Settings")
        verbose_name_plural = _("Space Settings")


class DefaultSpaceSettings(GameSettings):
    class Meta:
        verbose_name = _("Default Space Settings")
        verbose_name_plural = _("Default Space Settings")


class Snapshot(TimeStamped):
    state = jsonb.JSONField(_("Game State"), default={})
    game_time = models.FloatField(_("Game Time in Seconds"), default=0.0)
    game = models.ForeignKey("Game", null=True)
    space = models.ForeignKey("Space", null=True)
    settings = models.ForeignKey("SpaceSettings", null=True)

    def __init__(self, space):
        super(Snapshot, self).__init__()
        self.space = space
        self.game = space.game
        self.settings = space.settings
        self.game_time = 0.0
        self.new_state()

    def new_state(self):
        self.state = {}
        return self.state


class RandomSnapshot(Snapshot):

    def new_state(self):
        state = super(RandomSnapshot, self).new_state()
        state = self.add_random_asteroids(state)
        self.state = state
        return state

    def add_random_asteroids(self, state):
        game_settings = self.game.settings
        asteroid_count = game_settings.get_setting('asteroid_count', 100)
        asteroid_mass_min = game_settings.get_setting('asteroid_mass_min', 1.0)
        asteroid_mass_max = game_settings.get_setting('asteroid_mass_max', 100.0)
        # Would rather base radius off a random range of believable densities for an asteroid.
        asteroid_radius_min = game_settings.get_setting('asteroid_radius_min', 10.0)
        asteroid_radius_max = game_settings.get_setting('asteroid_radius_max', 50.0)
        asteroid_velocity_min = game_settings.get_setting('asteroid_velocity_min', 0.0)
        asteroid_velocity_max = game_settings.get_setting('asteroid_velocity_max', 30.0)

        for i in range(0, asteroid_count):
            mass = random.randrange(asteroid_mass_min, asteroid_mass_max)
            radius = random.randrange(asteroid_radius_min, asteroid_radius_max)
            position = self.get_random_position()
            velocity = RandomSnapshot.get_random_velocity(asteroid_velocity_min, asteroid_velocity_max)
            state['asteroids'].append({"mass": mass,
                                       "radius": radius,
                                       "position": position,
                                       "velocity": velocity})

        return state

    def get_random_position(self):
        return (random.randrange(self.space.space_min_x, self.space.space_max_x),
                random.randrange(self.space.space_min_y, self.space.space_max_y))

    @staticmethod
    def get_random_velocity(min_velocity, max_velocity):
        new_angle = random.uniform(0, math.pi*2)
        new_x = math.sin(new_angle)
        new_y = math.cos(new_angle)
        new_vector = numpy.array([new_x, new_y])
        new_vector.linalg.normalize()
        new_vector *= random.randrange(min_velocity, max_velocity)
        return new_vector


class Space(TimeStamped):
    class Meta:
        verbose_name = _("Space")
        verbose_name_plural = _("Spaces")
        ordering = ["-created"]

    game = models.ForeignKey("Game")
    initial_snapshot = models.ForeignKey("Snapshot", related_name="+")
    settings = models.ForeignKey("SpaceSettings")
    seed = models.CharField(_("Random Seed"), max_length=50)

    def __init__(self, game, settings=None, seed=None, random_state=True):
        if type(game) is not Game:
            raise TypeError
        if type(settings) is not SpaceSettings:
            raise TypeError
        super(Space, self).__init__()
        self.game = game
        self.settings = settings or DefaultSpaceSettings.objects.first()
        self.space_width = settings.get_setting('space_width', 100.0)
        self.space_depth = settings.get_setting('space_depth', 100.0)
        self.space_max_x = self.space_width/2
        self.space_min_x = -self.space_max_x
        self.space_max_y = self.space_depth/2
        self.space_min_y = -self.space_max_y
        self.seed = None
        self.game_space = None
        self.bodies = {}
        self.start_space(seed, random_state)

    @staticmethod
    def new_seed():
        string = "0123456789abcdef"
        seed = ""
        for i in range(0, 20):
            pos = random.randrange(0, len(string)-1)
            seed += string[pos]
        return seed
    
    def start_space(self, seed=None, random_state=True):
        self.seed = seed or Space.new_seed()
        random.seed(self.seed)
        self.game_space = pymunk.Space()
        if random_state:
            snapshot = self.start_random_snapshot()
        else:
            snapshot = self.start_new_snapshot()

        self.read_snapshot(snapshot)
        return self.game_space

    def start_new_snapshot(self):
        self.initial_snapshot = Snapshot(self)
        return self.initial_snapshot

    def start_random_snapshot(self):
        self.initial_snapshot = RandomSnapshot(self)
        return self.initial_snapshot

    def read_snapshot(self, snapshot):
        # Just reads in asteroids for now. Which are just circles.
        from .classes import Asteroid
        json_data = snapshot.state
        for asteroid_data in json_data['asteroids']:
            asteroid = Asteroid(self,
                                asteroid_data['radius'],
                                asteroid_data['mass'],
                                asteroid_data['position'],
                                asteroid_data['velocity'])
            self.bodies[asteroid.get_id()] = asteroid
        return snapshot
