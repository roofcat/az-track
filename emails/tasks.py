# -*- coding: utf-8 -*-


import logging


from app import celery_app
from utils.sendgrid_client import EmailClient


logger = logging.getLogger(__name__)


@celery_app.task
def input_queue(email):
    logger.info("Entrando a la cola de envío de email.")
    try:
        email_client = EmailClient(email.empresa_id)
        email_client.enviar_correo_dte(email)
    except Exception, e:
        logger.error(e)
