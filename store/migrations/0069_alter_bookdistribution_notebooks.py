# Generated by Django 3.2 on 2024-03-05 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0068_alter_bookdistribution_notebooks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookdistribution',
            name='notebooks',
            field=models.ManyToManyField(to='store.NotebookType', verbose_name='الكراسات المسلمة'),
        ),
    ]
