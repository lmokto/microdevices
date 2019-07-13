# microdevices
# microdevices
celery -A microdevices.celery worker -l info --queues=celery_periodic
****
celery -A microdevices worker -l info

$ mkdir -p /var/run/celery
$ mkdir -p /var/log/celery
$ celery multi start w1 -A proj -l info --pidfile=/var/run/celery/%n.pid \
                                        --logfile=/var/log/celery/%n%I.log