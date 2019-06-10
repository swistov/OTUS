# Generated by Django 2.2.1 on 2019-06-01 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appmain', '0006_auto_20190601_1934'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComputerType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
            ],
        ),
        migrations.AlterField(
            model_name='computer',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appmain.ComputerType'),
        ),
    ]