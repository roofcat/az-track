# -*- coding: utf-8 -*-


import base64
import logging


from sendgrid import SendGridAPIClient
from sendgrid.helpers import mail


from django.contrib.auth.models import User


from configuraciones.models import SendgridConf, TemplateReporte
from utils.generics import get_file_name_from_storage


logger = logging.getLogger(__name__)


class EmailClient(object):

    def __init__(self, empresa_id):
        self.empresa_id = empresa_id
        # llamar las configuraciones en la DB
        self.email_config = SendgridConf.get_sg_config(self.empresa_id)
        # crear los atributos de la instancia de SendGrid
        self.sg = SendGridAPIClient(api_key=self.email_config.api_key)
        self.message = mail.Mail()
        self.message.set_from(
            mail.Email(self.email_config.asunto_email_dte,
                  self.email_config.nombre_email_dte))
        self.personalization = mail.Personalization()

    def enviar_correo_dte(self, correo):
        # valores de envío
        self.personalization.add_to(mail.Email(correo.correo, correo.nombre_cliente))
        self.message.set_subject(correo.asunto)
        self.message.add_content(mail.Content(type="text/html", value=correo.html))
        # valores personalizados
        self.personalization.add_custom_arg(mail.CustomArg('email_id', str(correo.id)))
        self.personalization.add_custom_arg(mail.CustomArg('empresa', correo.empresa.rut))
        self.personalization.add_custom_arg(mail.CustomArg('rut_receptor', correo.rut_receptor))
        self.personalization.add_custom_arg(mail.CustomArg('rut_emisor', correo.rut_emisor))
        self.personalization.add_custom_arg(mail.CustomArg('tipo_envio', correo.tipo_envio))
        self.personalization.add_custom_arg(mail.CustomArg('tipo_dte', str(correo.tipo_dte.id_documento)))
        self.personalization.add_custom_arg(mail.CustomArg('numero_folio', str(correo.numero_folio)))
        self.personalization.add_custom_arg(mail.CustomArg('resolucion_receptor', str(correo.resolucion_receptor)))
        self.personalization.add_custom_arg(mail.CustomArg('resolucion_emisor', str(correo.resolucion_emisor)))
        self.personalization.add_custom_arg(mail.CustomArg('monto', str(correo.monto)))
        self.personalization.add_custom_arg(mail.CustomArg('fecha_emision', str(correo.fecha_emision)))
        self.personalization.add_custom_arg(mail.CustomArg('fecha_recepcion', str(correo.fecha_recepcion)))
        self.personalization.add_custom_arg(mail.CustomArg('estado_documento', correo.estado_documento))
        self.personalization.add_custom_arg(mail.CustomArg('tipo_operacion', correo.tipo_operacion))
        self.personalization.add_custom_arg(mail.CustomArg('tipo_receptor', correo.tipo_receptor))
        self.personalization.add_custom_arg(mail.CustomArg('id_envio', str(correo.id_envio)))

        logger.info(correo)
        
        if correo.xml:
            attach = mail.Attachment()
            attach.set_filename(get_file_name_from_storage(correo.xml.name))
            attach.set_content(base64.b64encode(correo.xml.file.read()))
            self.message.add_attachment(attach)
        if correo.pdf:
            attach = mail.Attachment()
            attach.set_filename(get_file_name_from_storage(correo.pdf.name))
            attach.set_content(base64.b64encode(correo.pdf.file.read()))
            self.message.add_attachment(attach)
        if correo.adjunto1:
            attach = mail.Attachment()
            attach.set_filename(get_file_name_from_storage(correo.adjunto1.name))
            attach.set_content(base64.b64encode(correo.adjunto1.file.read()))
            self.message.add_attachment(attach)
        self.message.add_personalization(self.personalization)
        # enviando el mail
        response = self.sg.client.mail.send.post(request_body=self.message.get())
        # imprimiendo respuesta
        logger.info(response.status_code)
        logger.info(response.headers)
        logger.info(response.body)

    def send_report_to_user_with_attach(self, user_email, report):
        # parametros de correo reporte
        self.message.set_from(
            mail.Email(self.email_config.asunto_email_reporte,
                  self.email_config.nombre_email_reporte))
        # buscar usuario
        template_config = TemplateReporte.get_configuration(self.empresa_id)
        # preparar template del correo reporte
        user = User.objects.get(email=user_email)
        html = str(template_config.template_html).format(
            user_name=user.first_name)
        # valores de envío
        self.personalization.add_to(mail.Email(user_email, user.first_name))
        self.message.set_subject(template_config.asunto_reporte)
        self.message.add_content(mail.Content(type="text/html", value=html))
        # adjuntar excel si esta
        if report['report']:
            attach = mail.Attachment()
            attach.set_content(base64.b64encode(report['report']))
            attach.set_filename(report['name'])
            self.message.add_attachment(attach)
        self.message.add_personalization(self.personalization)
        # enviando el correo
        response = self.sg.client.mail.send.post(request_body=self.message.get())
        # imprimiendo respuesta
        logger.info(response.status_code)
        logger.info(response.headers)
        logger.info(response.body)
