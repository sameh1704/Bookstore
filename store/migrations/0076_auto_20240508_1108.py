# Generated by Django 3.2 on 2024-05-08 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0075_alter_stockreport_academic_year'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockreport',
            old_name='class_levels',
            new_name='class_level',
        ),
        migrations.AlterUniqueTogether(
            name='stockreport',
            unique_together={('stage', 'class_level', 'academic_year', 'term')},
        ),
    ]
