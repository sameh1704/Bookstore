# Generated by Django 3.2 on 2024-02-25 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0061_alter_classlevel_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookdistribution',
            options={'verbose_name': 'توزيع الكتب والكراسات والبوكليتات', 'verbose_name_plural': 'توزيع الكتب والكراسات والبوكليتات'},
        ),
        migrations.AddField(
            model_name='bookdistribution',
            name='booklets',
            field=models.ManyToManyField(to='store.SchoolBooklet', verbose_name='البوكليتات المسلمة'),
        ),
        migrations.AddField(
            model_name='bookdistribution',
            name='notebooks',
            field=models.ManyToManyField(to='store.NotebookType', verbose_name='الكراسات المسلمة'),
        ),
        migrations.AddField(
            model_name='bookdistribution',
            name='recipient_name',
            field=models.CharField(default=1, max_length=100, verbose_name='اسم المستلم'),
            preserve_default=False,
        ),
    ]
