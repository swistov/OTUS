from django.shortcuts import render, HttpResponse
from django.views.generic import View, TemplateView

from . import models


class AppMainView(TemplateView):
    template_name = 'appmain/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        computer_type = models.ComputerType.objects.all()
        context.update({
            'computer_type': computer_type,
        })

        return context


class TypeView(TemplateView):
    template_name = 'appmain/type.html'

    def get_context_data(self, type_id, **kwargs):
        context = super().get_context_data(**kwargs)
        computers = models.Computer.objects.filter(type=type_id)
        context.update({
            'computers': computers,
        })

        return context


class ComputerView(TemplateView):
    template_name = 'appmain/computer.html'

    def get_context_data(self, computer_id, **kwargs):
        context = super().get_context_data(**kwargs)
        computer = models.Computer.objects.filter(pk=computer_id)
        context.update({
            'computer_info': computer,
        })

        return context
