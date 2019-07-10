from __future__ import absolute_import, unicode_literals
from celery import Celery


app = Celery('microdevices',
             broker='pyamqp://guest@172.17.0.2//',
             backend='rpc://',
             include=['microdevices.libs.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)



app.conf.timezone = 'UTC'

if __name__ == '__main__':
    app.start()
