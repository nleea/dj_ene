# Generated by Django 4.2.6 on 2023-10-25 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_rename_customer_id_workorder_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='workorder',
            name='type_order',
            field=models.CharField(choices=[('MANTENIMIENTO', 'Mantenimiento'), ('PLANEACION', 'Planeacion'), ('LIMPIEZA', 'Limpieza')], default='PLANEACION'),
        ),
    ]
