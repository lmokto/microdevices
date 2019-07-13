from .mock import Mock
from numpy.random import randint


class Devices(object):

    def __init__(self, name=None, lat=None, lng=None):
        """
        :param data:
        :param frequency:
        """
        self.name = name
        self.lat = lat
        self.lng = lng
        self.__id = int(''.join([str(n) for n in randint(0, 10, 10) if n]))
        self.sensors = []

    def get_id(self):

        return self.__id

    def get_fullname(self):
        id_name = '{name} -- {id}'.format(name=self.name, id=self.__id)
        return id_name

    def get_coords(self):
        return {
            'latitud': self.lat,
            'longitud': self.lng
        }

    def sensor(self, _id):
        """
        :param _id: 1
        :return: {'sensor1': 'data1'}
        """
        for sensor in self.sensors:
            if _id == sensor['id']:
                return sensor
        return {}

    def add(self, sensor):
        """
        :param _id:
        :param sensor:
        :return:
        """
        _id = getattr(sensor, 'name', str(sensor))
        if _id not in self.sensors:
            self.sensors.append({
                'id': _id,
                'register': sensor
            })
            return True
        return False

    def emit(self, _id):
        """
        :param _id:
        :return:
        """
        data = self.sensor(_id)['register'].get()
        if data:
            return data
        return None

    def remove(self, _id):
        """
        :param _id:
        :return:
        """
        for index, sensor in enumerate(self.sensors):
            if _id in sensor:
                del self.sensors[index]
            return True
        return False
