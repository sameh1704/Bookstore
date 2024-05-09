# Generated by Django 3.2 on 2024-02-22 08:03

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0056_alter_student_class_level'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='schoolsupplies',
            options={'verbose_name': 'ادوات   مدرسية', 'verbose_name_plural': 'الادوات المدرسية'},
        ),
        migrations.RemoveField(
            model_name='schoolsupplies',
            name='class_level',
        ),
        migrations.RemoveField(
            model_name='schoolsupplies',
            name='stage',
        ),
        migrations.AddField(
            model_name='schoolbooklet',
            name='booklet_edition',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='إصدار الكتاب'),
        ),
        migrations.AddField(
            model_name='schoolbooklet',
            name='received_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='تاريخ الاستلام'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schoolbooklet',
            name='source',
            field=models.CharField(choices=[('وزارة التربية والتعليم', 'وزارة التربية والتعليم'), (' مدرسة المنار', 'مدرسة المنار'), ('مورد خارجي', 'مورد خارجي')], default=1999, max_length=50, verbose_name='مصدر التوريد'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schoolbooklet',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.supplier', verbose_name='المورد'),
        ),
        migrations.AddField(
            model_name='schoolbooklet',
            name='term',
            field=models.CharField(choices=[('الترم الأول', 'الترم الأول'), ('الترم الثاني', 'الترم الثاني')], default=1999, max_length=20, verbose_name='الترم الدراسي'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schoolsupplies',
            name='received_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='تاريخ الاستلام'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schoolsupplies',
            name='source',
            field=models.CharField(choices=[('وزارة التربية والتعليم', 'وزارة التربية والتعليم'), ('مورد خارجي', 'مورد خارجي')], default=1999, max_length=50, verbose_name='مصدر التوريد'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schoolsupplies',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.supplier', verbose_name='المورد'),
        ),
        migrations.AddField(
            model_name='schoolsupplies',
            name='term',
            field=models.CharField(choices=[('الترم الأول', 'الترم الأول'), ('الترم الثاني', 'الترم الثاني')], default=1999, max_length=20, verbose_name='الترم الدراسي'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='available_quantity',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='الكمية المتاحة'),
        ),
        migrations.AlterField(
            model_name='book',
            name='received_date',
            field=models.DateField(auto_now_add=True, verbose_name='تاريخ الاستلام'),
        ),
        migrations.AlterField(
            model_name='book',
            name='received_quantity',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='الكمية الواردة'),
        ),
        migrations.AlterField(
            model_name='classlevel',
            name='name',
            field=models.CharField(choices=[('تمهيدى', 'تمهيدى'), ('KG1', 'KG1'), ('KG2', 'KG2'), ('PRIM 1', 'الصف  الأول الابتدائي '), ('PRIM 2', 'الصف الابتدائي الثاني'), ('PRIM 3', 'الصف الابتدائي الثالث'), ('PRIM 4', 'الصف الابتدائي الرابع'), ('PRIM 5', 'الصف الابتدائي الخامس'), ('PRIM 6', 'الصف الابتدائي السادس'), ('PREP 1', 'الصف الاعدادى الأول'), ('PREP 2', 'الصف الاعدادى الثاني'), ('PREP 3', 'الصف الاعدادى الثالث'), ('SEC 1', 'الصف الثانوي الأول'), ('SEC 2', 'الصف الثانوي الثاني'), ('SEC 3', 'الصف الثانوي الثالث')], max_length=50, verbose_name='اسم الصف الدراسي'),
        ),
        migrations.AlterField(
            model_name='schoolbooklet',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='وصف البوكليت'),
        ),
        migrations.AlterField(
            model_name='schoolbooklet',
            name='quantity',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='الكمية الواردة'),
        ),
        migrations.AlterField(
            model_name='schoolsupplies',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='وصف   الأداة المدرسية'),
        ),
        migrations.AlterField(
            model_name='schoolsupplies',
            name='name',
            field=models.CharField(max_length=100, verbose_name='   الأداة المدرسية'),
        ),
        migrations.AddConstraint(
            model_name='book',
            constraint=models.UniqueConstraint(fields=('title', 'source', 'term', 'stage', 'class_level'), name='unique_book_per_class'),
        ),
        migrations.AddConstraint(
            model_name='schoolbooklet',
            constraint=models.UniqueConstraint(fields=('title', 'booklet_edition', 'stage', 'class_level'), name='unique_booklet'),
        ),
        migrations.AddConstraint(
            model_name='schoolsupplies',
            constraint=models.UniqueConstraint(fields=('name', 'description'), name='unique_school_supplies'),
        ),
    ]
