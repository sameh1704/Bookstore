# Generated by Django 3.2 on 2024-01-24 15:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20240124_1754'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': 'الطالب', 'verbose_name_plural': 'اضافة الطلاب'},
        ),
        migrations.AlterField(
            model_name='student',
            name='class_level',
            field=models.CharField(choices=[], max_length=20, verbose_name='الصف الدراسي'),
        ),
        migrations.AlterField(
            model_name='student',
            name='national_id',
            field=models.CharField(default=1, max_length=14, validators=[django.core.validators.RegexValidator(code='invalid_national_id', message='يجب أن يحتوي الرقم القومي على 14 رقمًا بدقة.', regex='^\\d{14}$')], verbose_name='الرقم القومي'),
            preserve_default=False,
        ),
    ]
