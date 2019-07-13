try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

import ipdb

from datetime import datetime
import asyncio
import datetime

from sqlalchemy import create_engine

from .model import main

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


def handler_registry(args):
    """"""
    ipdb.set_trace()
    print('running registry', args.locate)


def fnc_handler(args):
    ipdb.set_trace()
    print('running handler', args)


def fnc_change(args):
    ipdb.set_trace()
    print('running change', args)


def fnc_active(args):
    ipdb.set_trace()
    print('running active', args)


def init_database(args):
    main()
    print('start database', args)