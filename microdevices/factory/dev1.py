import datetime
import threading

from microdevices.celery import app
from microdevices.libs.devices import Devices
from microdevices.libs.sensors import Sensor

voltage = Sensor(name='voltage', freq=2, dynamic=True, **{'type': 'int'})
consumption = Sensor(name='consumption', freq=4, dynamic=True, **{
    'type': 'int', 'low': 20, 'high': 40, 'size': 1
})

# Instanciamos los sensores al Dispositivo
dev = Devices(name='dev1')
dev.add(consumption)
dev.add(voltage)

WAIT_TASK_CONS = 5
WAIT_TASK_VOLT = 2
# Emitimos datos segun sensor

@app.task(name='factory.dev1.dev1_task_consumption')
def dev1_task_consumption():
    """
        In [21]: dev1_task_consumption()
        2019-07-12 18:39:17.843953 38
        ...
    """
    ticker = threading.Event()
    while True:
        # connect to mqtt and push data
        print(dev.get_id(), 'consumption', datetime.datetime.now(), dev.emit('consumption'))
        # wait utilizar conector, variable de redis
        ticker.wait(WAIT_TASK_CONS)


@app.task(name='factory.dev1.dev1_task_voltage')
def dev1_task_voltage():
    """
        In [21]: dev1_task_consumption()
        2019-07-12 18:39:17.843953 38
        ...
    """
    ticker = threading.Event()
    while True:
        # connect to mqtt and push data
        print(dev.get_id(), 'voltage', datetime.datetime.now(), dev.emit('voltage'))
        # wait utilizar conector, variable de redis
        ticker.wait(WAIT_TASK_VOLT)


registry = [{
    'id': dev.get_id(),
    'class': dev,
    'tasks': [{
        'status': 'inactive',
        'fnc': dev1_task_consumption,
        'interval': WAIT_TASK_CONS,
    },{
        'status': 'inactive',
        'fnc': dev1_task_voltage,
        'interval': WAIT_TASK_VOLT,
    }]
}]
