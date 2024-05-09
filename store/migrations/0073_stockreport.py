# Generated by Django 3.2 on 2024-04-29 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0072_auto_20240424_1147'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(choices=[('الترم الأول', 'الترم الأول'), ('الترم الثاني', 'الترم الثاني')], max_length=20, verbose_name='الترم الدراسي')),
                ('report_date', models.DateField(auto_now_add=True, verbose_name='تاريخ التقرير')),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.academicyear', verbose_name='السنة الدراسية')),
                ('class_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.classlevel', verbose_name='الصف الدراسي')),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.stage', verbose_name='المرحلة الدراسية')),
            ],
            options={
                'verbose_name': 'تقرير المخزون',
                'verbose_name_plural': 'تقارير المخزون',
                'unique_together': {('stage', 'class_level', 'academic_year', 'term')},
            },
        ),
    ]