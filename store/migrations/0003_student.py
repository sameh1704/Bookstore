# Generated by Django 3.2 on 2024-01-24 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20240124_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='اسم الطالب')),
                ('national_id', models.CharField(max_length=14, verbose_name='الرقم القومي')),
                ('class_level', models.CharField(max_length=20, verbose_name='الصف الدراسي')),
                ('section', models.CharField(blank=True, max_length=2, null=True, verbose_name='الفصل الدراسي')),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.stage', verbose_name='المرحلة الدراسية')),
            ],
        ),
    ]