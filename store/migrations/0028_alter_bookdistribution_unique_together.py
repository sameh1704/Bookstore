# Generated by Django 3.2 on 2024-02-06 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_auto_20240202_2337'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookdistribution',
            unique_together={('student', 'delivery_date', 'receipt_number')},
        ),
    ]