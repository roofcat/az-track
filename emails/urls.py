# -*- coding: utf-8 -*-


from django.conf.urls import url


from .views import SendDelayedEmails


urlpatterns = [
    url(r'enviar-pendientes/', SendDelayedEmails.as_view()),
]
