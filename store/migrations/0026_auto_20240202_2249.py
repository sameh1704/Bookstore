# Generated by Django 3.2 on 2024-02-02 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_alter_book_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookdistribution',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='bookdistribution',
            unique_together=set(),
        ),
    ]
