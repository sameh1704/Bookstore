# Generated by Django 3.2 on 2024-01-31 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_remove_classroom_class_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stage',
            name='class_levels',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.classlevel', verbose_name='الصف الدراسي'),
        ),
    ]