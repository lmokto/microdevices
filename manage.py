import argparse
import sys

from microdevices.libs.utils import (
    handler_registry, fnc_handler, fnc_change, init_database, handler_inspect, handler_launch
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///microdevices.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

"""
	Creamos una funciones templates ( que reciban los parametros enviado por consola)
		Debe emitir datos cada un intervalo de tiempo segun cada dispositivo
		Ejemplo.

			A. Ambos valores pueden ser cambiados en tiempo real.
                1. voltage emite datos cada 2 segundos
				2. consumption emite datos cada 5 segundos
			B. Los datos deben ser enviado segun el conector
				1. mqtt
				2. redis
				3. api (aws o otras plataformas)

			C. Cada funcion debe ser registrada como un task en Celery (Done)

			1.
            python manage.py registry --device=<factory.dev1.registry>
            	Aqui registramos un device y sus tareas asociadas
            	    id (id unique) 123132
            	    device (device asociado) dev1
            	    task (id task celery) (una ves iniciado) (default None)
            	    fnc (referencia para ubicar su funcion) (¿ubicacion?) + name factory.dev1.dev1_task_voltage
            	    status (si esta activa o no la funcion) (inactive default) (active cuando esta iniciado) inactive
            2.
            python manage.py inspect --device=<dev1> (nos da la info de todas las tareas registradas de un device)

            3.
            python manage.py launch --action=<start|stop|pause> --task=<id>
            	Aqui debemos poder iniciar las tasks, detenerlas o pausarlas, al iniciarla debemos almacenar
            	1. verifciar que la tarea esta inactiva y registrada
            	2. verificar que podemos ejecutar la tarea (porque esta en el modulo)
            	3. verificar que la tarea esta en la pila de ejecucion de celery
            	resultado de ejecutar tarea, nos da un id que debemos guardar
            	su id de celery y cambiar su status, en la tabla
            	    1. iniciamos una tarea especifcia del device
            4.
            python manage.py change=<interval|otro> --value=1 --task=<dev1_task_consumption>
            	Aqui podremos cambiar parametros de configuracion de la task en tiempo de ejecucion

"""

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()


# Create a template for active devices subcommand
# python manage.py start_db

parser_active = subparsers.add_parser('start_db', help='start database tables')
parser_active.set_defaults(func=init_database)

# Create a template for registry devices subcommand
# python manage.py factory --registry='factory.dev1.registry'
# python manage.py factory --registry='factory.dev2.registry'

parser_registry = subparsers.add_parser('factory', help='It provide an interface to register devices.')
parser_registry.add_argument('--registry', help='relative path registry dict')
parser_registry.set_defaults(func=handler_registry) # change

# python manage.py inspect --device='dev2'
# python manage.py inspect --device='dev1'

parser_registry = subparsers.add_parser('inspect', help='It provide an interface to inspect devices.')
parser_registry.add_argument('--device', help='It name of device to inspect')
parser_registry.set_defaults(func=handler_inspect) # change

# Create a template for handler devices subcommand
parser_action = subparsers.add_parser('launch', help='manage status of devices')
parser_action.add_argument('--action', help='select the action to devices start|stop|pause')
parser_action.add_argument('--task', help='device name registry')
parser_action.set_defaults(func=handler_launch)

# Create a template for change devices subcommand
parser_change = subparsers.add_parser('change', help='change running time the time to push data')
parser_change.add_argument('--value', help='value to change setinterval')
parser_change.add_argument('--task', help='task id celery')
parser_change.set_defaults(func=fnc_change)


# handler_inspect

if len(sys.argv) <= 1:
    sys.argv.append('--help')

options = parser.parse_args()
# Run the appropriate function (in this case showtop20 or listapps)
options.func(options, session)
