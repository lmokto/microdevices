try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

import ipdb

from datetime import datetime
import asyncio
import datetime

from .model import main, TableRegistry


# https://stackoverflow.com/questions/8884188/how-to-read-and-write-ini-file-with-python3
class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def instance_config(filename):
    """
    :param filename:
    :return: class config
    """
    config = ConfigParser(dict_type=AttrDict)
    try:
        config.read(filename)
        return config._sections
    except:
        return []


async def display_date():
    """
        emite datos cada 1 segundo durante 5 segundos.
        In [5]: asyncio.run(display_date()
        2019-07-12 18:24:17.763086
        2019-07-12 18:24:18.763789
        2019-07-12 18:24:19.765581
        ...
    """
    loop = asyncio.get_running_loop()
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)


def locate_registry(locate):
    """
    :param locate: 'factory.dev1.registry'
    :return: 'dev1'
    """
    paths = locate.split('.')
    for k in paths:
        if k in ['factory', 'registry']:
            paths.remove(k)
    return paths[0] if paths else []


def verify_devices(dev):
    """
    :param dev: 'dev1'
    :return: True | False
    """
    try:
        from microdevices import factory
    except:
        raise ValueError('microdevices factory not found')
    else:
        modules = dir(factory)
        if dev in modules:
            return True
        return False


def verify_task(task, dev):
    """
    :param task: dev1_task_consumption
    :param dev: dev1
    :return: True
    """
    try:
        import microdevices.factory
        devices = getattr(microdevices.factory, dev)
    except:
        raise ValueError('microdevices factory not found')
    else:
        functions = dir(devices)
        if task in functions:
            return True
        return False


def return_registry(dev):
    """
    :param dev: dev1
    :return: [{'id':123123' ... , 'tasks':[{..}]}]
    """
    from microdevices import factory
    module = getattr(factory, dev)
    registry = getattr(module, 'registry')
    return registry


def filter_tasks(device, session):
    """
    :param device:
    :param session:
    :return:
    """
    filter_dev = []
    try:
        devices = session.query(TableRegistry).filter_by(device=device)
        for dev in devices:
            filter_dev.append(dev.__dict__)
    except:
        session.rollback()
    finally:
        print(filter_dev)
        return filter_dev


def insert_tasks(locate, session):
    """
    :param locate: 'factory.dev1.registry'
    :param session: session
    :return: [{..},{...}]
    """
    module = locate_registry(locate)
    assert verify_devices(module)
    session_add = []
    try:
        registries = return_registry(module)
        for devices in registries:
            _name = devices['class'].name
            _tasks = devices['tasks']
            for task in _tasks:
                registry = TableRegistry(
                    device=_name,
                    path=locate,
                    interval=task['interval'],
                    task=None,
                    fnc=task['fnc'].name,
                    status=task['status']
                )
                session.add(registry)
                session_add.append(registry.__dict__)
        session.commit()
    except:
        session.rollback()
    finally:
        print(session_add)
        return session_add


def handler_registry(args, session):
    """
    :param args:
    :param session:
    :return:
    """
    session_add = insert_tasks(args.registry, session)
    return session_add


def handler_launch(args, session):
    """
    :param args:
    :param session:
    :return:
    """
    resp = None
    if args.action == 'start':
        resp = start_task(args.task, session)
    elif args.action == 'stop':
        resp = stop_task(args.task, session)
    elif args.action == 'pause':
        resp = pause_task(args.task, session)
    return resp


def get_task(registries, fnc):
    """
    :param registries:
    :param fnc:
    :return:
    """
    for devices in registries:
        _tasks = devices['tasks']
        for _task in _tasks:
            if _task['fnc'].name == fnc:
                return _task['fnc']
    return False


def start_task(_id, session):
    """
    :param _id:
    :param session:
    :return:
        1. verificar que este registrada + inactiva
        2. verificar que la tarea este en el modulo
        3. verificar que este en celery
        4. iniciar
        5. cambiar estado y actualizar id

    """
    try:
        task = session.query(TableRegistry).filter_by(id=_id, status='inactive').first()
        registries = return_registry(task.device)
        invoke_task = get_task(registries, task.fnc)
        result = invoke_task.delay()
        response = update_task(session, _id, **{'status': 'active', 'task': result.id})
        return response
    except:
        return False


def stop_task(_id, session):
    pass


def pause_task(_id, session):
    pass


def update_task(session, _id, **kwargs):
    """
    :param session: session
    :param _id: 3
    :param kwargs: {'status': 'active'}
    :return:
    """
    task = session.query(TableRegistry).filter_by(id=_id).first()
    assert task
    for k, v in kwargs.items():
        setattr(task, k, v)
    session.commit()
    return task


def handler_inspect(args, session):
    """
    :param args:
    :param session:
    :return:
    """
    session_get = filter_tasks(args.device, session)
    return session_get


def fnc_handler(args):
    ipdb.set_trace()
    print('running handler', args)


def fnc_change(args):
    ipdb.set_trace()
    print('running change', args)


def fnc_active(args):
    ipdb.set_trace()
    print('running active', args)


def init_database(args, session=None):
    """
    :param args:
    :param session:
    :return:
    """
    main()
    print('start database', args)
