# Generated by Django 2.1.3 on 2019-09-10 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_basebone', '0006_auto_20190910_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filter',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='条件字段名'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='value',
            field=models.CharField(max_length=100, null=True, verbose_name='条件值'),
        ),
    ]