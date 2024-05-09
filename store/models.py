from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from django.db.models.signals import post_save
from django.db import transaction
from django.db.models import UniqueConstraint
from django.core.validators import MinValueValidator




#######################################################################
class AcademicYear(models.Model):
    year = models.IntegerField(unique=True, verbose_name="السنة الدراسية")
    
    def __str__(self):
        return str(self.year)
    class Meta:
        verbose_name = 'السنة'
        verbose_name_plural = '  السنة الدراسية'


class Stage(models.Model):
    STAGE_CHOICES = [
        ('تمهيدى', 'تمهيدى'),
        ('رياض الأطفال', 'رياض الأطفال'),
        ('primry', 'primry'),
        ('الاعدادية', 'الاعدادية'),
        ('الثانوية', 'الثانوية'),
    ]
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES, verbose_name='المرحلة الدراسية')
    

   
    def __str__(self):
        return f"{self.stage} "

    class Meta:
        unique_together = ['stage']
        verbose_name = 'المرحلة'
        verbose_name_plural = 'المراحل الدراسية'


    class Meta:
        unique_together = ['stage']
        verbose_name = 'المرحلة'
        verbose_name_plural = 'المراحل الدراسية'
    
    
class ClassLevel(models.Model):
    class_choices = [
        ('تمهيدى', 'تمهيدى'),
        ('KG1', 'KG1'),
        ('KG2', 'KG2'),
        ('PRIM 1', 'الصف  الأول الابتدائي '),
        ('PRIM 2', 'الصف الابتدائي الثاني'),
        ('PRIM 3', 'الصف الابتدائي الثالث'),
        ('PRIM 4', 'الصف الابتدائي الرابع'),
        ('PRIM 5', 'الصف الابتدائي الخامس'),
        ('PRIM 6', 'الصف الابتدائي السادس'),
        ('PREP 1', 'الصف الاعدادى الأول'),
        ('PREP 2', 'الصف الثاني الاعدادى '),
        ('PREP 3', 'الصف الثالث الاعدادى '),
        ('SEC 1', 'الصف الأول الثانوي '),
        ('SEC 2', 'الصف الثاني الثانوي '),
        ('SEC 3', 'الصف الثالث الثانوي '),
    ]
    name = models.CharField(max_length=50, choices=class_choices, verbose_name='اسم الصف الدراسي')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name='المرحلة')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, verbose_name="السنة الدراسية")

    def __str__(self):
        return self.name

    class Meta:
        unique_together = [['stage', 'name', 'academic_year']]
        verbose_name = 'الصف'
        verbose_name_plural = 'الصف الدراسي'


class Classroom(models.Model):
    name = models.CharField(max_length=2, verbose_name='الفصل الدراسي')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name='المرحلة')
    class_levels = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, verbose_name='الصف الدراسي')

    def __str__(self):
        return f"{self.name} "

    class Meta:
        unique_together = [['class_levels', 'name']]
        verbose_name = 'ترقيم الفصول'
        verbose_name_plural = 'الفصل الدراسي'




##########################################################################################################################


class Student(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, verbose_name="السنة الدراسية", related_name="students")
    name = models.CharField(max_length=255, verbose_name='اسم الطالب')
    national_id = models.CharField(
        max_length=14,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{14}$',
                message='يجب أن يحتوي الرقم القومي على 14 رقمًا بدقة.',
                code='invalid_national_id'
            )
        ],
        verbose_name='الرقم القومي'
    )
    phone_number = models.CharField(max_length=15, verbose_name='رقم الهاتف')  # قمت بإضافة هذا الحقل
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name='المرحلة الدراسية')
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, verbose_name='الصف الدراسي')
    section = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=True, null=True, verbose_name='الفصل الدراسي')


    def migrate_to_next_level(self):
        # استخراج قائمة اختيارات الصفوف الدراسية في المرحلة الحالية
        current_stage_class_choices = [c[0] for c in self.stage.classlevel_set.all().values_list('name')]

        # التحقق من كون الطالب في الصف الأخير في المرحلة
        if self.class_level.name == current_stage_class_choices[-1]:
            # الترحيل إلى المرحلة التالية
            next_stage = Stage.objects.filter(
                classlevel__name=self.class_level.name,
                stage__gt=self.stage.stage
            ).first()

            if next_stage:
                next_class_level = next_stage.classlevel_set.first()  # الصف الدراسي الأول في المرحلة التالية
                self.stage = next_stage
                self.class_level = next_class_level
                self.section = None  # إعادة الطالب إلى الفصل الدراسي الافتراضي
                self.academic_year = str(int(self.academic_year) + 1)  # زيادة العام الدراسي بمقدار واحد

        else:
            # الترحيل إلى الصف التالي في نفس المرحلة
            next_class_level_name = current_stage_class_choices[current_stage_class_choices.index(self.class_level.name) + 1]
            next_class_level = self.stage.classlevel_set.get(name=next_class_level_name)
            self.class_level = next_class_level



    def save(self, *args, **kwargs):
        if not self.pk:
            academic_year, created = AcademicYear.objects.get_or_create(year='2023')
            self.academic_year = academic_year  # تعيين العام الدراسي إلى العام الحالي
        else:
            if self.academic_year.year != '2023':  # إذا لم يكن العام الدراسي الحالي هو العام الحالي
                self.migrate_to_next_level()  # ترحيل الطالب
        super().save(*args, **kwargs)


    def clean(self):
        # التحقق من عدم تكرار الرقم القومي داخل السنة الدراسية نفسها
        students_with_same_national_id = Student.objects.filter(national_id=self.national_id, academic_year=self.academic_year).exclude(id=self.id)
        if students_with_same_national_id.exists():
            raise ValidationError({'national_id': 'هذا الرقم القومي موجود بالفعل في سجلات الطلاب.'})

        # التحقق من أن رقم الهاتف يحتوي على أكثر من 12 رقم وأنه يتكون من أرقام فقط
        if len(self.phone_number) < 11:
            raise ValidationError(_('رقم الهاتف يجب أن يحتوي على 11 رقم على الأقل.'))
        if not self.phone_number.isdigit():
            raise ValidationError(_('رقم الهاتف يجب أن يتكون من أرقام فقط.'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'الطالب'
        verbose_name_plural = 'اضافة الطلاب'


##########################################################################################################################

class Supplier(models.Model):
    name = models.CharField(max_length=100, verbose_name='اسم المورد')
    phone = models.CharField(max_length=15, verbose_name='رقم تليفون المورد')

    def __str__(self):
        return f"{self.name} - {self.phone}"

    class Meta:
        verbose_name = 'مورد'
        verbose_name_plural = 'الموردين'

#############################################################################################################################


class Book(models.Model):
    TITLE_CHOICES = [
        ('ARABIC', 'ARABIC'),
        ('MATH', 'MATH'),
        ('Science', 'Science'),
        ('History', 'History'),
        ('Islamic Studies', 'Islamic Studies'),
        ('Art', 'Art'),
        ('Music', 'Music'),
        ('English OL', 'English OL'),
        ('English AL', 'English AL'),
        ('French', 'French'),
        ('Computer Science', 'Computer Science'),
        ('Philosophy', 'Philosophy'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
        ('Biology', 'Biology'),
        # ... أي مواد أخرى
    ]

    SOURCE_CHOICES = [
        ('وزارة التربية والتعليم', 'وزارة التربية والتعليم'),
        ('مورد خارجي', 'مورد خارجي'),
    ]

    TERM_CHOICES = [
        ('الترم الأول', 'الترم الأول'),
        ('الترم الثاني', 'الترم الثاني'),
    ]

    title = models.CharField(max_length=50, choices=TITLE_CHOICES, verbose_name='المادة الدراسية')
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, verbose_name='مصدر التوريد')
    received_quantity = models.PositiveIntegerField(verbose_name='الكمية الواردة', validators=[MinValueValidator(0)])
    available_quantity = models.PositiveIntegerField(verbose_name='الكمية المتاحة',)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True, verbose_name='المورد')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name='المرحلة الدراسية')
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, verbose_name='الصف الدراسي')
    term = models.CharField(max_length=20, choices=TERM_CHOICES, verbose_name='الترم الدراسي')
    received_date = models.DateField(auto_now_add=True, verbose_name='تاريخ الاستلام')

    def save(self, *args, **kwargs):
        if not self.id:
            self.available_quantity = self.received_quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.get_title_display()} - {self.source} - {self.term} - Available Quantity: {self.available_quantity}'

    class Meta:
        verbose_name = 'كتاب دراسي'
        verbose_name_plural = 'المواد الدراسية'
        constraints = [
            UniqueConstraint(fields=['title', 'source', 'term', 'stage', 'class_level'], name='unique_book_per_class')
        ]



class SchoolBooklet(models.Model):
    SOURCE_CHOICES = [
        ('وزارة التربية والتعليم', 'وزارة التربية والتعليم'),
        (' مدرسة المنار', 'مدرسة المنار'),
        ('مورد خارجي', 'مورد خارجي'),
    ]

    TERM_CHOICES = [
        ('الترم الأول', 'الترم الأول'),
        ('الترم الثاني', 'الترم الثاني'),
    ]
    
    title = models.CharField(max_length=100, verbose_name='عنوان البوكليت')
    booklet_edition = models.CharField(max_length=20, verbose_name='إصدار الكتاب', blank=True, null=True)
    description = models.TextField(verbose_name='وصف البوكليت', blank=True, null=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, verbose_name='مصدر التوريد')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True, verbose_name='المورد')
    stage = models.ForeignKey('Stage', on_delete=models.CASCADE, verbose_name='المرحلة الدراسية')
    class_level = models.ForeignKey('ClassLevel', on_delete=models.CASCADE, verbose_name='الصف الدراسي')
    quantity = models.IntegerField(default=0, verbose_name='الكمية الواردة', validators=[MinValueValidator(0)])
    live_quantity = models.IntegerField(default=0, verbose_name='الكمية الحالية')
    term = models.CharField(max_length=20, choices=TERM_CHOICES, verbose_name='الترم الدراسي')
    received_date = models.DateField(auto_now_add=True, verbose_name='تاريخ الاستلام')

    def save(self, *args, **kwargs):
        if not self.id:
            self.live_quantity = self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} - {self.source} - {self.term} - الكمية الحالية : {self.live_quantity}'

    class Meta:
        verbose_name = 'بوكليت مدرسي'
        verbose_name_plural = 'البوكليتات المدرسية'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'booklet_edition', 'stage', 'class_level'],
                name='unique_booklet'
            )
        ]




class SchoolSupplies(models.Model):
    SOURCE_CHOICES = [
        ('وزارة التربية والتعليم', 'وزارة التربية والتعليم'),
        ('مورد خارجي', 'مورد خارجي'),
    ]

    TERM_CHOICES = [
        ('الترم الأول', 'الترم الأول'),
        ('الترم الثاني', 'الترم الثاني'),
    ]
    name = models.CharField(max_length=100, verbose_name='   الأداة المدرسية')
    description = models.TextField(verbose_name='وصف   الأداة المدرسية', blank=True, null=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, verbose_name='مصدر التوريد')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True, verbose_name='المورد')
    in_quantity = models.IntegerField(default=0, verbose_name='الكمية الواردة')
    live_quantity = models.IntegerField(default=0, verbose_name='الكمية الحالية')
    term = models.CharField(max_length=20, choices=TERM_CHOICES, verbose_name='الترم الدراسي')
    received_date = models.DateField(auto_now_add=True, verbose_name='تاريخ الاستلام')


    def save(self, *args, **kwargs):
        if not self.id:
            self.live_quantity = self.in_quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'ادوات   مدرسية'
        verbose_name_plural = 'الادوات المدرسية'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'description'],
                name='unique_school_supplies'
            )
        ]
#######################################################################################################3
class NotebookType(models.Model):
    SOURCE_CHOICES = [
        ('وزارة التربية والتعليم', 'وزارة التربية والتعليم'),
        ('مورد خارجي', 'مورد خارجي'),
    ]

    TERM_CHOICES = [
        ('الترم الأول', 'الترم الأول'),
        ('الترم الثاني', 'الترم الثاني'),
    ]

    name = models.CharField(max_length=100, verbose_name='نوع الكراسة')
    size = models.CharField(max_length=50, verbose_name='حجم الكراسة')
    description = models.CharField(max_length=100, verbose_name='وصف الكراسة', blank=True, null=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, verbose_name='مصدر التوريد')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True, verbose_name='المورد')
    in_quantity = models.IntegerField(default=0, verbose_name='الكمية الواردة')
    live_quantity = models.IntegerField(default=0, verbose_name='الكمية الحالية')
    term = models.CharField(max_length=20, choices=TERM_CHOICES, verbose_name='الترم الدراسي')
    received_date = models.DateField(auto_now_add=True, verbose_name='تاريخ الاستلام')

    
    def decrement_quantity(self):
        if self.live_quantity > 0:
            self.live_quantity -= 1
            self.save()
        else:
            raise ValidationError("لا يوجد رصيد كافٍ لهذه الكراسة")
    
    def increment_quantity(self):
       self.live_quantity += 1
       self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            self.live_quantity = self.in_quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.size}'

    class Meta:
        verbose_name = 'نوع كراسة'
        verbose_name_plural = 'أنواع الكراسات'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'size'],
                name='unique_notebook_type'
            )
        ]


class NotebookAssignment(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name='المرحلة الدراسية')
    grade = models.ForeignKey('ClassLevel', on_delete=models.CASCADE, verbose_name='الصف الدراسي')
    notebook = models.ForeignKey(NotebookType, on_delete=models.CASCADE, verbose_name='الكراسة')
    quantity_assignment = models.PositiveIntegerField(default=0, verbose_name='الكمية المخصصة')
    year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, verbose_name="السنة الدراسية")
    assigned_date = models.DateField(auto_now_add=True, verbose_name='تاريخ التخصيص')
    

    def __str__(self):
        return f'{self.grade} - {self.notebook.name} - {self.quantity_assignment}'

    class Meta:
        verbose_name = 'تخصيص كراسة'
        verbose_name_plural = 'تخصيصات الكراسات'
        




#######################################################################################################################

class BookDistribution(models.Model):
    PARTIAL_DISTRIBUTION = 'جزئي'
    FULL_DISTRIBUTION = 'كامل'
    DISTRIBUTION_CHOICES = [
        (PARTIAL_DISTRIBUTION, 'توزيع جزئي'),
        (FULL_DISTRIBUTION, 'توزيع كامل'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='الطالب')
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name='المرحلة الدراسية')
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, verbose_name='الصف الدراسي')
    section = models.ForeignKey(Classroom, on_delete=models.CASCADE, verbose_name='الفصل الدراسي')
    receipt_number = models.CharField(max_length=20, verbose_name='رقم الإيصال')
    
    books = models.ManyToManyField(Book, verbose_name='الكتب المسلمة', blank=True)
    notebooks = models.ManyToManyField(NotebookType, verbose_name='الكراسات المسلمة', blank=True)
    booklets = models.ManyToManyField(SchoolBooklet, verbose_name='البوكليتات المسلمة', blank=True)

    delivery_date = models.DateField(auto_now_add=False, verbose_name='تاريخ التوزيع')
    distribution_status = models.CharField(max_length=20, choices=DISTRIBUTION_CHOICES, default=FULL_DISTRIBUTION, verbose_name='حالة التوزيع')
    recipient_name = models.CharField(max_length=100, verbose_name='اسم المستلم')

    
    def get_books_titles(self):
        return ", ".join([book.title for book in self.books.all()])

    def get_notebooks_titles(self):
        return ", ".join([notebook.name for notebook in self.notebooks.all()])

    def get_booklets_titles(self):
        return ", ".join([booklet.title for booklet in self.booklets.all()])  # دالة للحصول على أسماء البوكليتات

    #def display_status(self):
        #return "تم التسليم بالكامل" if self.is_delivered_completely else "لم يتم التسليم بالكامل"
    
    

    def __str__(self):
        return f'{self.student.name} - {self.stage} - {self.class_level} - {self.receipt_number}'

    class Meta:
        verbose_name = 'توزيع الكتب والكراسات والبوكليتات'
        verbose_name_plural = 'توزيع الكتب والكراسات والبوكليتات'
        unique_together = ['student', 'delivery_date', 'receipt_number']

  # إضافة استقبال لتغييرات البوكليتات
@receiver(m2m_changed, sender=BookDistribution.books.through) 
def update_books_quantity(sender, instance, action, **kwargs):
    if action == 'post_add':
        for book in instance.books.all():
            if book.available_quantity > 0:
                book.available_quantity -= 1
                book.save()

    elif action == 'post_remove':
        for book in instance.books.all():
            book.available_quantity += 1
            book.save()
@receiver(m2m_changed, sender=BookDistribution.booklets.through)
def update_booklets_quantity(sender, instance, action, **kwargs):
    if action == 'post_add':
        for booklet in instance.booklets.all():
            if booklet.live_quantity > 0:
                booklet.live_quantity -= 1
                booklet.save()

    elif action == 'post_remove':
        for booklet in instance.booklets.all():
            booklet.live_quantity += 1
            booklet.save()


@receiver(m2m_changed, sender=BookDistribution.notebooks.through)  
def update_quantities(sender, instance, action, **kwargs):
    if action == 'post_add':
        for notebook in instance.notebooks.all():
            notebook.decrement_quantity()
            
    if action == 'post_remove':   
        for notebook in instance.notebooks.all():
            notebook.increment_quantity()

#######################################################################################################################

from django.db.models import Sum

class StockReport(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, verbose_name='المرحلة الدراسية')
    class_level = models.ForeignKey(ClassLevel, on_delete=models.CASCADE, verbose_name='الصف الدراسي')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, verbose_name='السنة الدراسية', related_name='stock_reports')
    term = models.CharField(max_length=20, choices=Book.TERM_CHOICES, verbose_name='الترم الدراسي')
    report_date = models.DateField(auto_now_add=True, verbose_name='تاريخ التقرير')

    def __str__(self):
        return f"{self.stage} - {self.class_levels} - {self.academic_year} - {self.term}"

    class Meta:
        verbose_name = 'تقرير المخزون'
        verbose_name_plural = 'تقارير المخزون'
        unique_together = ('stage', 'class_level', 'academic_year', 'term')

    @property
    def total_books_received(self):
        return Book.objects.filter(
            stage=self.stage,
            class_level=self.class_levels,
            term=self.term
        ).aggregate(total=Sum('received_quantity'))['total'] or 0

    @property
    def total_books_issued(self):
        return sum(book.received_quantity - book.available_quantity for book in Book.objects.filter(
            stage=self.stage,
            class_level=self.class_levels,
            term=self.term
        ))

    @property
    def total_notebooks_assigned(self):
        return sum(assignment.quantity_assignment for assignment in NotebookAssignment.objects.filter(
            stage=self.stage,
            grade=self.class_levels,
            year=self.academic_year
        ))

    @property
    def total_notebooks_issued(self):
        return NotebookType.objects.filter(
            notebookassignment__stage=self.stage,
            notebookassignment__grade=self.class_levels,
            notebookassignment__year=self.academic_year
        ).aggregate(total_issued=Sum('notebookassignment__quantity_assignment') - Sum('live_quantity'))['total_issued'] or 0

    @property
    def total_notebooks_received(self):
        return NotebookType.objects.filter(
            stage=self.stage,
            class_level=self.class_levels,
            term=self.term
        ).aggregate(total=Sum('in_quantity'))['total'] or 0

    @property
    def total_notebooks_available(self):
        return sum(notebook.live_quantity for notebook in NotebookType.objects.filter(
            stage=self.stage,
            class_level=self.class_levels,
            term=self.term
        ))

    @property
    def total_booklets_received(self):
        return SchoolBooklet.objects.filter(
            stage=self.stage,
            class_level=self.class_levels,
            term=self.term
        ).aggregate(total=Sum('quantity'))['total'] or 0

    @property
    def total_booklets_issued(self):
        return sum(booklet.quantity - booklet.live_quantity for booklet in SchoolBooklet.objects.filter(
            stage=self.stage,
            class_level=self.class_levels,
            term=self.term
        ))

    @property
    def total_supplies_received(self):
        return SchoolSupplies.objects.filter(term=self.term).aggregate(total=Sum('in_quantity'))['total'] or 0

    @property
    def total_supplies_issued(self):
        return sum(supply.in_quantity - supply.live_quantity for supply in SchoolSupplies.objects.filter(term=self.term))

    @property
    def total_students(self):
        return Student.objects.filter(
            stage=self.stage,
            class_level=self.class_levels
        ).count()
