# Generated by Django 3.2 on 2024-02-13 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0034_alter_book_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={},
        ),
        migrations.AddField(
            model_name='bookdistribution',
            name='distribution_status',
            field=models.CharField(choices=[('جزئي', 'توزيع جزئي'), ('كامل', 'توزيع كامل')], default='كامل', max_length=20, verbose_name='حالة التوزيع'),
        ),
        migrations.AlterField(
            model_name='bookdistribution',
            name='is_delivered_completely',
            field=models.BooleanField(default=False, verbose_name='تم التسليم بالكامل'),
        ),
    ]
