# Generated by Django 3.2 on 2024-05-05 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0074_auto_20240505_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockreport',
            name='academic_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_reports', to='store.academicyear', verbose_name='السنة الدراسية'),
        ),
    ]
