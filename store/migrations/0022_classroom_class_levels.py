# Generated by Django 3.2 on 2024-02-02 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_auto_20240202_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='class_levels',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.classlevel', verbose_name='الصف الدراسي'),
            preserve_default=False,
        ),
    ]