from mock import Mock


class Sensor(object):
    data = None
    freq = 0
    dynamic = False
    random = None

    def __init__(self, name, data=None, freq=0, dynamic=False, **config):
        """
        :param data:
        :param frequency:
        """
        self.name = name
        if dynamic:
            self.dynamic = True
            self.random = Mock(**config)
        self.set_frequency(freq)
        self.set_data(data)

    def set_data(self, data):
        """
        :param data:
        :return:
        """
        self.data = data

    def get(self):
        if self.dynamic:
            return self.random.generate()
        return self.data

    def set_frequency(self, frequency=0):
        """
        :param frequency:
        :return:
        """
        if frequency:
            self.freq = frequency
        return self.freq


class Devices(object):

    def __init__(self):
        """
        :param data:
        :param frequency:
        """
        self.sensors = []

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


def sensor_factory():
    # Creamos los sensores
    voltage = Sensor(name='voltage', freq=2, dynamic=True)
    consumption = Sensor(name='consumption', freq=4, dynamic=True, **{'low': 20, 'high': 40, 'size': 1})

    # Instanciamos los sensores al Dispositivo
    dev = Devices()
    dev.add(consumption)
    dev.add(voltage)

    # Emitimos datos segun sensor
    dev.emit('consumption')
    dev.emit('voltage')
