import numpy


class Body(object):
    class Meta:
        abstract = True

    __nextId = 1

    @staticmethod
    def next_id():
        next_id = Body.__nextId
        Body.__nextId += 1
        return next_id

    def __init__(self):
        self.__id = Body.next_id()
        self.time = 0.0
        self.mass = 0.0
        self.vector = numpy.array([0, 0])
        self.acceleration = numpy.array([0, 0])
        self.location = numpy.array([0, 0])

    def updated_location(self, dtime=None):
        if dtime is not None:
            return self.location + (self.vector * dtime) + 0.5*(self.acceleration * (dtime ** 2))
        else:
            return self.location

    def update_position(self, dtime):
        self.location = self.updated_location(dtime)
        return self.location

    def updated_vector(self, dtime=None):
        if dtime is not None:
            return self.vector + (self.acceleration * dtime)
        else:
            return self.vector

    def update_vector(self, dtime):
        self.vector = self.updated_vector(dtime)
        return self.vector

    def update(self, dtime):
        self.update_position(dtime)
        self.update_vector(dtime)


class RoundBody(Body):
    class Meta:
        abstract = True

    def __init__(self):
        super(RoundBody, self).__init__()
        self.radius = 0.0


class Asteroid(RoundBody):
    pass


class Ship(Body):
    __nextShipId = 1

    @staticmethod
    def next_ship_id():
        next_id = Ship.__nextShipId
        Ship.__nextShipId += 1
        return next_id

    def __init__(self):
        super(Ship, self).__init__()
        self.ship_id = Ship.next_ship_id()
        self.name = None
        self.player = None


