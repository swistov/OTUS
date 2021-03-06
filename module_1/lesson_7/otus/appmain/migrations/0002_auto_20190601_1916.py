# Generated by Django 2.2.1 on 2019-06-01 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appmain', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComputerManufacture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='computer',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.CreateModel(
            name='ComputerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('manufacturer', models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='appmain.ComputerManufacture')),
            ],
        ),
    ]
