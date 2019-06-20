# noinspection PyPackageRequirements
"""
    Primer Sensor
        1. una funcion para emitir datos fake entre n and x
        https://docs.scipy.org/doc/numpy/reference/routines.random.html

        2. creemos una funcion que muestre los datos en consola cada un intervalo
        3. realicemos que celery ejecute de manera asyncrona la funcion del punto 2
"""

import numpy as np


def generate_random(low, high, size):
    """
    :param low: int 10
    :param high: int 20
    :param size: int 1
    :return: 20
    """
    return np.random.randint(
        low=low, high=high, size=size
    )[0]

