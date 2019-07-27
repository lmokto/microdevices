from __future__ import absolute_import, unicode_literals
from celery import Celery

app = Celery('microdevices',
             broker='redis://localhost:6379/0',
             backend='rpc://',
             include=[
                 'microdevices.factory.dev1',
                 'microdevices.factory.dev2'
             ]
             )

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

app.conf.timezone = 'UTC'

if __name__ == '__main__':
    app.start()
