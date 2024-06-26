# Generated by Django 3.2 on 2024-02-19 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0042_alter_bookdistribution_receipt_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='academic_year',
        ),
        migrations.AddField(
            model_name='classlevel',
            name='academic_year',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='store.academicyear', verbose_name='السنة الدراسية'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='stage',
            name='class_levels',
        ),
        migrations.AddField(
            model_name='stage',
            name='class_levels',
            field=models.ManyToManyField(to='store.ClassLevel', verbose_name='الصف الدراسي'),
        ),
        migrations.AlterField(
            model_name='stage',
            name='stage',
            field=models.CharField(choices=[('تمهيدى', 'تمهيدى'), ('رياض الأطفال', 'رياض الأطفال'), ('الابتدائية', 'الابتدائية'), ('الاعدادية', 'الاعدادية'), ('الثانوية', 'الثانوية')], max_length=50, verbose_name='المرحلة الدراسية'),
        ),
    ]
