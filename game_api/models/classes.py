import numpy
from Box2D import *
from .models import Space


class Body(object):
    class Meta:
        abstract = True

    __nextId = 1

    @staticmethod
    def next_id():
        next_id = Body.__nextId
        Body.__nextId += 1
        return next_id

    def __init__(self, space, mass=1.0, position=numpy.array([0, 0]), velocity=numpy.array([0, 0])):
        if type(space) is not Space:
            raise TypeError
        self.__id = Body.next_id()
        self.time = 0.0
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.acceleration = numpy.array([0, 0])
        self.space = space

    def get_id(self):
        return self.__id

    # Don't think I'll need any of this anymore now that I'm using pymunk for simulating the physics
    def updated_position(self, dtime=None):
        if dtime is not None:
            return self.position + (self.velocity * dtime) + 0.5*(self.acceleration * (dtime ** 2))
        else:
            return self.position

    def update_position(self, dtime):
        self.position = self.updated_position(dtime)
        return self.position

    def updated_velocity(self, dtime=None):
        if dtime is not None:
            return self.velocity + (self.acceleration * dtime)
        else:
            return self.velocity

    def update_velocity(self, dtime):
        self.velocity = self.updated_velocity(dtime)
        return self.velocity

    def accelerate(self, acceleration, dtime):
        self.velocity += acceleration * dtime
        return self.velocity

    def thrust(self, thrust):
        pass

    def get_force(self):
        return self.mass * self.velocity

    def update(self, dtime):
        self.update_position(dtime)
        self.update_velocity(dtime)


class RoundBody(Body):
    class Meta:
        abstract = True

    def __init__(self, space, radius, mass=None, position=None, velocity=None):
        super(RoundBody, self).__init__(space, mass, position, velocity)
        self.radius = radius
        self.game_body = space.game_space.CreateDynamicBody(position=position, mass=mass)
        self.game_shape = self.game_body.CreateCircleFixture(radius=radius, friction=0.2, density=1.0)
        self.game_body.linearVelocity = velocity


class PolyBody(Body):
    class Meta:
        abstract = True

    def __init__(self, space, vertices, mass=None, position=None, velocity=None):
        super(PolyBody, self).__init__(space, mass, position, velocity)
        self.vertices = vertices
        self.game_shape = b2PolygonShape(vertices=vertices)
        self.game_body = space.game_space.CreateDynamicBody(position=position,
                                                            mass=mass,
                                                            shapes=self.game_shape)
        self.game_body.linearVelocity = velocity


class Asteroid(RoundBody):
    pass


class Ship(Body):
    __nextShipId = 1

    @staticmethod
    def next_ship_id():
        next_id = Ship.__nextShipId
        Ship.__nextShipId += 1
        return next_id

    def __init__(self, space):
        super(Ship, self).__init__(space)
        self.ship_id = Ship.next_ship_id()
        self.name = None
        self.player = None


