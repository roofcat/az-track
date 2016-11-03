# -*- coding: utf-8 -*-


"""
Módulo de configuración de las tareas que puedan
ser creadas y ejecutadas en la aplicación.
(requiere de RabbitMQ-Server)
"""


from __future__ import absolute_import


import os


from django.conf import settings
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')


app = Celery('track')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    BROKER_URL='amqp://guest:guest@localhost//',
    CELERY_ACEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
)
