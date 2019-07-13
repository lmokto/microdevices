import argparse
import sys
import ipdb


def fnc_registry(args):
    ipdb.set_trace()
    print('running registry', args)

def fnc_handler(args):
    ipdb.set_trace()
    print('running handler', args)

def fnc_change(args):
    ipdb.set_trace()
    print('running change', args)

def fnc_active(args):
    ipdb.set_trace()
    print('running active', args)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

# Create a template for registry devices subcommand    
parser_registry = subparsers.add_parser('registry', help='registry devices')
parser_registry.add_argument('--device', help='device name registry')
parser_registry.set_defaults(func=fnc_registry) # change

# Create a template for handler devices subcommand   
parser_action = subparsers.add_parser('handler', help='hangler status of devices')
parser_action.add_argument('--action', help='select the action to devices start|stop|pause')
parser_action.add_argument('--device', help='device name registry')
parser_action.set_defaults(func=fnc_handler)

# Create a template for change devices subcommand   
parser_change = subparsers.add_parser('change', help='change running time the time to push data')
parser_change.add_argument('--value', help='value to change setinterval')
parser_change.add_argument('--task', help='task id celery')
parser_change.set_defaults(func=fnc_change)

# Create a template for active devices subcommand   
parser_active = subparsers.add_parser('active', help='show all tasks or devices active')
parser_active.add_argument('--type', help='select the type task|dev')
parser_active.set_defaults(func=fnc_active)


if len(sys.argv) <= 1:
    sys.argv.append('--help')

options = parser.parse_args()
# Run the appropriate function (in this case showtop20 or listapps)
options.func(options)

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
            	Aqui registramos una devices y sus tareas asociadas

            2.
            python manage.py handler --action=<start|stop|pause> --device=<dev1>
            	Aqui debemos poder iniciar las tasks, detenerlas o pausarlas
            	al iniciarla debemos almacenar su id de celery y mapearlo con el registro previo
            3.
            python manage.py change=<interval|otro> --value=1 --task=<dev1_task_consumption>
            	Aqui podremos cambiar parametros de configuracion de la task en tiempo de ejecucion

            python manage.py active --type=<task|dev>
            	Aqui mostramos todas las task (funciones que emiten datos a conectores) activas segun el dispositivos
            	debemos tener un mapeo de dispositivo y task registradas por celery


"""
