from microdevices.libs.devices import Sensor, Devices


def main():
    voltage = Sensor(name='voltage', freq=2, dynamic=True, **{'type': 'int'})
    consumption = Sensor(name='consumption', freq=4, dynamic=True, **{'type': 'int', 'low': 20, 'high': 40, 'size': 1})

    # Instanciamos los sensores al Dispositivo
    dev = Devices()
    dev.add(consumption)
    dev.add(voltage)
    # Emitimos datos segun sensor
    dev.emit('consumption')
    dev.emit('voltage')
