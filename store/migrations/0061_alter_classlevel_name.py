# Generated by Django 3.2 on 2024-02-22 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0060_auto_20240222_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classlevel',
            name='name',
            field=models.CharField(choices=[('تمهيدى', 'تمهيدى'), ('KG1', 'KG1'), ('KG2', 'KG2'), ('PRIM 1', 'الصف  الأول الابتدائي '), ('PRIM 2', 'الصف الابتدائي الثاني'), ('PRIM 3', 'الصف الابتدائي الثالث'), ('PRIM 4', 'الصف الابتدائي الرابع'), ('PRIM 5', 'الصف الابتدائي الخامس'), ('PRIM 6', 'الصف الابتدائي السادس'), ('PREP 1', 'الصف الاعدادى الأول'), ('PREP 2', 'الصف الثاني الاعدادى '), ('PREP 3', 'الصف الثالث الاعدادى '), ('SEC 1', 'الصف الأول الثانوي '), ('SEC 2', 'الصف الثاني الثانوي '), ('SEC 3', 'الصف الثالث الثانوي ')], max_length=50, verbose_name='اسم الصف الدراسي'),
        ),
    ]