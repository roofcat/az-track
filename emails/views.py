# -*- coding: utf-8 -*-


from datetime import date, timedelta
import logging


from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView


from rest_framework import authentication, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Email
from .serializers import EmailDteInputSerializer, EmailTrackDTESerializer
from .tasks import input_queue
from configuraciones.models import EliminacionHistorico
from empresas.models import Empresa


logger = logging.getLogger(__name__)


class EmailDteInputView(APIView):
    """ Vista encargada de recibir los request vía post para crear nuevos email
        y enviarlos por correo utilizando SendGrid
    """
    # authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = EmailDteInputSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        # Método que permite consultar el estado de un correo.
        logger.info(request.query_params)
        query_params = request.query_params
        params = dict()

        try:
            # Validar si vienen parametros en el GET
            params['correo'] = query_params['correo']
            params['numero_folio'] = query_params['numero_folio']
            params['tipo_dte'] = query_params['tipo_dte']
            params['rut_emisor'] = query_params['rut_emisor']
            params['resolucion_emisor'] = query_params['resolucion_emisor']
            params['id_envio'] = query_params['id_envio']
            # imprimiendo parametros
            logger.info(params)
            # consulta
            email = Email.get_email(**params)
            # imprimir resultado de la consulta
            logger.info(email)
            if email is not None:
                logger.info("no es vacio")
                # serializar
                response = EmailTrackDTESerializer(email, many=False)
                # responder
                return Response(response.data)
            else:
                logger.info("es vacio")
                return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception, e:
            return Response({"mensaje": "Error en parametros enviados."})

    def post(self, request, format=None):
        """ Método que permite el input de un correo para ser
            gestionado por el Track.
        """
        email = EmailDteInputSerializer(data=request.data)

        if email.is_valid():
            email.save()
            logger.info(email.data)
            correo = Email.objects.get(pk=email.data['id'])
            input_queue(correo)
            return Response({'status': 200})
        else:
            logger.error(email.errors)
            return Response(email.errors)


class CronCleanEmailsHistoryView(TemplateView):
    """ Método que si tiene habilitada la opción de eliminar correos antiguos
        antiguos (parametrizado en app configuraciones) lista los correos
        desde el numero de meses máximo a retener en la DB.
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CronCleanEmailsHistoryView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Listar todas las configuraciones activas
        active_configs = EliminacionHistorico.objects.filter(activo=True)

        # Recorrer listado
        for config in active_configs:
            if config.activo:
                if config.dias_a_eliminar is not None:
                    try:
                        # resta la fecha de hoy con los días a eliminar
                        today = date.today()
                        days = timedelta(days=config.dias_a_eliminar)
                        date_to_delete = today - days
                        # listar las empresas al holding que pertenece la conf actual
                        empresas = Empresa.objects.filter(holding=config.holding)
                        for empresa in empresas:
                            # enviar la petición para borrar
                            emails = Email.delete_old_emails_by_date(date_to_delete, empresa)
                    except Exception, e:
                        logger.error(e)
                        return HttpResponse(e)
        return HttpResponse()


class CronSendDelayedEmailView(TemplateView):
    """ Evalúa los correos que no se han podido enviar,
        los correos que caen en este proceso son aquellos que son
        ingresados vía json post en el servicio rest publicado
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CronSendDelayedEmailView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logger.info("entrando a la cola de reenvio de correos")
        logger.info(request.body)
        emails = Email.get_delayed_emails()
        if emails is not None:
            for email in emails:
                input_queue(email)
        return HttpResponse()


class CronSendDelayedProcessedEmailView(TemplateView):
    """ Esta es la vista que reintenta envíos de correos
        cuando se utiliza la api de tracking para enviar
        correos de los DTEs
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(CronSendDelayedProcessedEmailView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logger.info("entrando a la cola de reenvio de correos")
        logger.info(request.body)
        emails = Email.get_delayed_emails_only_processed()
        if emails is not None:
            for email in emails:
                input_queue(email)
        return HttpResponse()
