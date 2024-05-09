# Generated by Django 3.2 on 2024-02-13 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0033_alter_classlevel_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(choices=[('ARABIC', 'ARABIC'), ('MATH', 'MATH'), ('Science', 'Science'), ('History', 'History'), ('Islamic Studies', 'Islamic Studies'), ('Art', 'Art'), ('Music', 'Music'), ('English OL', 'English OL'), ('English AL', 'English AL'), ('French', 'French'), ('Computer Science', 'Computer Science'), ('Philosophy', 'Philosophy'), ('Physics', 'Physics'), ('Chemistry', 'Chemistry'), ('Biology', 'Biology')], max_length=50, verbose_name='المادة الدراسية'),
        ),
    ]