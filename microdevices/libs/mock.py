import numpy as np
import random

from shapely.geometry import Point
from shapely.geometry import Polygon


class Mock(object):
    """
        mock = Mock(**{'type':'int','low': 20, 'high': 40, 'size': 1})
        mock.get()
    """
    low = 0
    size = 0
    high = 0

    polygon = None
    minx = None
    miny = None
    maxx = None
    maxy = None

    coords = [(41.403596, 2.150574), (41.389173, 2.122335), (41.376937, 2.161388)]
    randint = False
    randcoords = False

    def __init__(self, **config):
        """
        :param low:
        :param high:
        :param size:
        """
        if config.get('type') == 'int':
            self.randint = True
            self.set_params(config.get('low', 10), config.get('high', 20), config.get('size', 1))
        elif config.get('type') == 'coords':
            self.polygon = self.set_coords(config.get('coords', None))
            self.minx, self.miny, self.maxx, self.maxy = self.polygon.bounds
            self.randcoords = True
        else:
            raise ValueError('')

    def set_coords(self, coords):
        if coords:
            polygon = Polygon(coords)
        else:
            polygon = Polygon(self.coords)
        return polygon

    def set_params(self, low, high, size):
        """
        :param low:
        :param high:
        :param size:
        :return:
        """
        self.low = low
        self.high = high
        self.size = size

    def generate(self):
        """
        :param low: int 10
        :param high: int 20
        :param size: int 1
        :return: 20
        """
        if self.randint:
            return self.random_int()
        elif self.randcoords:
            return self.random_coords()
        else:
            return None

    def random_int(self):
        data = np.random.randint(low=self.low, high=self.high, size=self.size)
        if self.size == 1:
            return data[0]
        return data

    def random_coords(self):
        """
        :param number: 10
        :param polygon: polygon = Polygon([(0, 0), (1, 1), (1, 0)])
        :return:
        """
        list_of_points = []
        counter = 0
        while counter < 10:
            pnt = Point(random.uniform(self.minx, self.maxx), random.uniform(self.miny, self.maxy))
            if self.polygon.contains(pnt):
                list_of_points.append({'lat': pnt.x, 'long': pnt.y})
                counter += 1
        return list_of_points[random.randrange(0, 10)]
