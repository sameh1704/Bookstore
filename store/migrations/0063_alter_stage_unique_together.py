# Generated by Django 3.2 on 2024-02-26 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0062_auto_20240225_1052'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='stage',
            unique_together={('stage',)},
        ),
    ]