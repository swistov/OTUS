# Generated by Django 2.2.1 on 2019-06-01 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appmain', '0005_auto_20190601_1933'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='computer',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='computermanufacture',
            options={'ordering': ['id']},
        ),
    ]
