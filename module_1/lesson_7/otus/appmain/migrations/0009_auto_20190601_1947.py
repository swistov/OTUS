# Generated by Django 2.2.1 on 2019-06-01 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appmain', '0008_auto_20190601_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='type',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='appmain.ComputerType'),
        ),
    ]