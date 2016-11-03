# -*- coding: utf-8 -*-


from django.contrib import admin


from .models import Empresa, Holding, CamposOpcionalesEmail


class HoldingAdmin(admin.ModelAdmin):
    list_filter = ('nombre',)
    search_fields = ('nombre',)


class EmpresaAdmin(admin.ModelAdmin):
    list_filter = ('rut', 'empresa',)
    search_fields = ('rut', 'empresa',)


class CamposOpcionalesEmailAdmin(admin.ModelAdmin):
    list_filter = ('empresa',)
    search_fields = ('empresa',)


admin.site.register(Holding, HoldingAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(CamposOpcionalesEmail, CamposOpcionalesEmailAdmin)
