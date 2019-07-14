from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine

Base = declarative_base()

"""
[{
    'id': 581664338,
    'name': 'voltage'
}]
"""


class TableDevices(Base):

    __tablename__ = 'devices'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Device(id='%s', name='%s')>" % (self.id, self.name)
"""
[{
    'id': 581664338,
    'class': "<microdevices.libs.devices.Devices object at 0x7fbcc1be0c88>",
    'tasks': [
        {
            'name': "<@task: microdevices.factory.dev1.dev1_task_consumption of microdevices at 0x7fbcc22b87f0>",
            'interval': 5,
            'status':'active'
        }, {
            'name': "<@task: microdevices.factory.dev1.dev1_task_voltage of microdevices at 0x7fbcc22b87f0>",
            'interval': 2,
            'status':'active'
        }
    ]
}]

"""
class TableRegistry(Base):
    __tablename__ = 'registry'

    id = Column(Integer, primary_key=True)
    device = Column(String)
    path = Column(String)
    interval = Column(String)
    task = Column(String)
    fnc = Column(String)
    status = Column(String)

    def __repr__(self):
        return "<Registry(id='%s', task='%s', fnc='%s')>" % (self.id, self.task, self.fnc)


def main():
    engine = create_engine('sqlite:///microdevices.db', echo=True)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    main()
