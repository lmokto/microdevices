from __future__ import absolute_import, unicode_literals
from celery import Celery

"""
Clase que instance 1.

Configuracion de celery para cada dispositivo

Creacion clase dispositivo (abstractos)
creacion de metodos con sensores (abstractos)

---

exchange
queue
routing

--
instanciamos la clase

1. configuracion de tipo de sensores
2. configuracion del tipo de datos que enviara el sensor y el rango de datos (min, max)
3. configuracion de la periodicidad del envio de dato
4. configuracion de conector

de momento cada app celery debe ser un dispositivo que pueda consumir diferentes colas donde los sensores emitiran los datos

1. cada dispositivo sera instanciado en supervisor
2. cada sensor de cada dispositivo sera instanciado como tareas asyncronas en celery

3. cada dispositivo manejara manera periodica segun el intervalo especificado el llamado a emitir datos segun su sensor...
    ejemplo, el dispositivo que mide el clima emitira
        humedad: 10 segundos
        sensasion termica: cada 2 minutos
        viento: cada 1 hora

4. los sensores emitiran los datos algun lugar...

---

Caso de uso dispositivo
    dipositivo
        sensores1 (humedad) -> cola1
        sensores2 (temperatura) -> cola2
        sensores1 (presion) -> cola3

"""


app = Celery('microdevices',
             broker='pyamqp://guest@172.17.0.2//',
             backend='rpc://',
             include=['microdevices.libs.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

#
# app.conf.beat_schedule = {
#     "emit-generate-random": {
#         "task": "microdevices.libs.tasks.emit",
#         "schedule": 10.0,
#         "options": {
#             'queue': "celery_periodic"
#         }
#     }
# }


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')
    # Calls test('world') every 30 seconds
    pass


app.conf.timezone = 'UTC'

if __name__ == '__main__':
    app.start()
