# Generated by Django 3.2 on 2024-02-27 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0065_remove_notebookassignment_remaining_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='available_quantity',
            field=models.IntegerField(default=0, verbose_name='الكمية المتاحة'),
        ),
    ]