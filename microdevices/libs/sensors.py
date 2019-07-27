from .mock import Mock


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
