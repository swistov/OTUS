from django.contrib import admin

from .models import Computer, ComputerModel, ComputerManufacture, ComputerType


@admin.register(Computer)
class ArticleAdmin(admin.ModelAdmin):

    def body_short(self, obj: Computer):
        return f'{obj.body[:30]}...'

    list_display = ['id', 'type', 'name', 'body_short']


@admin.register(ComputerModel)
class ComputerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(ComputerManufacture)
class ComputerManufactureAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(ComputerType)
class ComputerTypeAdmin(admin.ModelAdmin):
    pass
