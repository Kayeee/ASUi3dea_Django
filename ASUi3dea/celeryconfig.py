from celery import Celery 
from kombu import Queue

CELERY_DEFAULT_QUEUE = 'interface'
CELERY_QUEUES = (Queue('interface', routing_key='interface.add'), Queue('updater', routing_key='updater.updateAurora'),)

