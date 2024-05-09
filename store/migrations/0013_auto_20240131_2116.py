# Generated by Django 3.2 on 2024-01-31 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20240131_2047'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='class_level',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='class_level',
        ),
        migrations.RemoveField(
            model_name='stage',
            name='section',
        ),
        migrations.AddField(
            model_name='classroom',
            name='class_levels',
            field=models.ManyToManyField(to='store.ClassLevel', verbose_name='الصفوف الدراسية'),
        ),
        migrations.AddField(
            model_name='stage',
            name='class_levels',
            field=models.ManyToManyField(to='store.ClassLevel', verbose_name='الصفوف الدراسية'),
        ),
        migrations.AddField(
            model_name='stage',
            name='classrooms',
            field=models.ManyToManyField(to='store.Classroom', verbose_name='الفصول الدراسية'),
        ),
    ]