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
        raise ValueError('microdeivces.factory not found')
    else:
        modules = dir(factory)
        if dev in modules:
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


def insert_tasks(locate, session):
    """
    :param args:
    :param kwargs:
    :return:
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
    insert_tasks(args.locate, session)


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
    main()
    print('start database', args)
