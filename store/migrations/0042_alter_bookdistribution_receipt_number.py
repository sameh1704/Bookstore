# Generated by Django 3.2 on 2024-02-19 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0041_alter_bookdistribution_receipt_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookdistribution',
            name='receipt_number',
            field=models.CharField(max_length=20, verbose_name='رقم الإيصال'),
        ),
    ]
