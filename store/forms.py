from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.utils import timezone
from .models import AcademicYear, ClassLevel, Classroom, Stage, Student, Supplier, Book, BookDistribution
from .models import BookDistribution
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import BookDistribution, Book, NotebookType, SchoolBooklet, Stage, ClassLevel, Classroom
from django.forms import ValidationError
from django import forms
from .models import NotebookType
from django import forms
from .models import NotebookAssignment
from .models import SchoolBooklet
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import SchoolSupplies
##########################################################################################################
class ClassLevelForm(forms.ModelForm):
    class Meta:
        model = ClassLevel
        fields = ['name', 'stage', 'academic_year']

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError('يرجى إدخال اسم الصف.')
        if not name.strip().replace(" ", "").isalpha():
            raise forms.ValidationError('اسم الصف يجب أن يحتوي على أحرف فقط.')
        return name

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'class_levels']

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError('يرجى إدخال اسم الفصل.')
        return name

class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['stage']

    def clean(self):
        cleaned_data = super().clean()
        stage = cleaned_data.get('stage')
        academic_year = cleaned_data.get('academic_year')

        if stage and academic_year:
            if stage == 'رياض الأطفال' and academic_year.year != 1:
                raise forms.ValidationError('خطأ: رياض الأطفال يجب أن يكون الصف الوحيد في السنة الدراسية الأولى.')

        return cleaned_data

##############################################################################################################################
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'national_id', 'phone_number', 'stage', 'class_level', 'section', 'academic_year']

    def clean_national_id(self):
        national_id = self.cleaned_data['national_id']
        if not national_id.isdigit():
            raise forms.ValidationError('الرقم القومي يجب أن يحتوي على أرقام فقط.')
        return national_id
######################################################################################################################

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'phone']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise forms.ValidationError('رقم الهاتف يجب أن يحتوي على أرقام فقط.')
        return phone
###################################################################################################################################3

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'source', 'received_quantity', 'supplier', 'stage', 'class_level', 'term']

    def clean_received_date(self):
        received_date = self.cleaned_data['received_date']
        if received_date < timezone.now().date():
            raise ValidationError('لا يمكنك تحديد تاريخ في الماضي.')
        return received_date

    def clean(self):
        super().clean()
        stage = self.cleaned_data.get('stage')
        class_level = self.cleaned_data.get('class_level')
        if stage and class_level:
            # التحقق من أن الصف الدراسي المحدد يتناسب مع المرحلة
            if not class_level.stage == stage:
                raise ValidationError('الصف الدراسي المحدد لا يتناسب مع المرحلة المحددة.')

###########################################################################################################################33


class NotebookTypeForm(forms.ModelForm):
    class Meta:
        model = NotebookType
        fields = ['name', 'size', 'description', 'source', 'supplier', 'in_quantity', 'term']

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        size = cleaned_data.get('size')
        # التحقق من عدم تكرار البيانات
        if NotebookType.objects.filter(name=name, size=size).exists():
            raise forms.ValidationError('هذا النوع من الكراسات موجود بالفعل.')
        return cleaned_data
######################################################################################################3


class NotebookAssignmentForm(forms.ModelForm):
    class Meta:
        model = NotebookAssignment
        fields = ['stage', 'grade', 'notebook', 'quantity_assignment', 'year']

    def clean(self):
        cleaned_data = super().clean()
        notebook = cleaned_data.get('notebook')
        quantity_assignment = cleaned_data.get('quantity_assignment')
        if notebook and quantity_assignment:
            if quantity_assignment > notebook.live_quantity:
                raise forms.ValidationError('الكمية المخصصة أكبر من الكمية المتاحة للكراسة.')
        return cleaned_data


####################################################################################################################################3



class SchoolBookletForm(forms.ModelForm):
    class Meta:
        model = SchoolBooklet
        fields = ['title', 'booklet_edition', 'description', 'source', 'supplier', 'stage', 'class_level', 'quantity', 'term']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'stage' in self.data:
            try:
                stage_id = int(self.data.get('stage'))
                self.fields['class_level'].queryset = ClassLevel.objects.filter(stage_id=stage_id)
            except (ValueError, TypeError):
                pass  # يتم تجاهل أي خطأ هنا

    def clean(self):
        cleaned_data = super().clean()
        stage = cleaned_data.get('stage')
        class_level = cleaned_data.get('class_level')
        term = cleaned_data.get('term')
        title = cleaned_data.get('title')

        if stage and class_level and term:
            # التحقق من عدم تكرار البوكيلت لنفس الصف الدراسي في نفس الترم
            if SchoolBooklet.objects.filter(stage=stage, class_level=class_level, term=term).exclude(title=title).exists():
                raise forms.ValidationError('هذا البوكليت موجود بالفعل لنفس الصف الدراسي في نفس الترم.')
            
            # التحقق من الكمية
            quantity = cleaned_data.get('quantity')
            if quantity < 0:
                raise forms.ValidationError('الكمية يجب أن تكون أكبر من أو تساوي الصفر.')

        return cleaned_data

####################################################################################################################################3
    


class SchoolSuppliesForm(forms.ModelForm):
    class Meta:
        model = SchoolSupplies
        fields = ['name', 'description', 'source', 'supplier', 'in_quantity', 'term']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        description = cleaned_data.get('description')
        term = cleaned_data.get('term')

        if name and description:
            # التحقق من عدم تكرار تسجيل الأدوات
            if SchoolSupplies.objects.filter(name=name, description=description).exists():
                raise forms.ValidationError('هذه الأداة المدرسية مسجلة بالفعل.')

        # التحقق من الكمية
        in_quantity = cleaned_data.get('in_quantity')
        if in_quantity < 0:
            raise forms.ValidationError('الكمية يجب أن تكون أكبر من الصفر.')

        return cleaned_data



####################################################################################################################################3





# فورم البحث عن الطالب
class StudentSearchForm(forms.Form):
    student_name = forms.CharField(label='اسم الطالب', max_length=255)

    def __init__(self, *args, **kwargs):
        super(StudentSearchForm, self).__init__(*args, **kwargs)
        self.fields['student_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ادخل اسم الطالب'})
        
# فورم اختيار الطالب
class StudentSelectForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name']

    def __init__(self, *args, **kwargs):
        students = kwargs.pop('students')  # استخراج الطلاب من الوسيطة
        super(StudentSelectForm, self).__init__(*args, **kwargs)
        # إعداد اختيار الطالب المحدد لاستخدامه في القائمة المنسدلة
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].queryset = students

    # إضافة دالة clean لتحديث حقول المرحلة والصف والفصل بالقيم الصحيحة عند اختيار الطالب
    def clean(self):
        cleaned_data = super().clean()
        selected_student = cleaned_data.get('name')
        if selected_student:
            cleaned_data['stage'] = selected_student.stage
            cleaned_data['class_level'] = selected_student.class_level
            cleaned_data['section'] = selected_student.section

# فورم توزيع الكتب والكراسات والبوكليتات

class BookDistributionForm(forms.ModelForm):
    search_student = forms.CharField(label='ابحث عن الطالب', max_length=255, required=True)
    receipt_number = forms.CharField(label='رقم ايصال الدفع', required=True)

    # تحديد حقول الكتب والكراسات والبوكليتات غير ملزمة
    books = forms.ModelMultipleChoiceField(queryset=Book.objects.all(), widget=forms.SelectMultiple, required=False)
    notebooks = forms.ModelMultipleChoiceField(queryset=NotebookType.objects.all(), widget=forms.SelectMultiple, required=False)
    booklets = forms.ModelMultipleChoiceField(queryset=SchoolBooklet.objects.all(), widget=forms.SelectMultiple, required=False)
    stage = forms.ModelChoiceField(queryset=Stage.objects.all(), required=True, label='المرحلة الدراسية')
    class_level = forms.ModelChoiceField(queryset=ClassLevel.objects.all(), required=True, label='الصف الدراسي')
    section = forms.ModelChoiceField(queryset=Classroom.objects.all(), required=True, label='الفصل الدراسي')
    delivery_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}), required=True, label='تاريخ التوزيع')

    def __init__(self, *args, **kwargs):
        super(BookDistributionForm, self).__init__(*args, **kwargs)
        self.fields['delivery_date'].initial = timezone.now().date()

    def clean_receipt_number(self):
        receipt_number = self.cleaned_data.get('receipt_number')
        delivery_date = self.cleaned_data.get('delivery_date')

        if not receipt_number:
            raise forms.ValidationError('يرجى إدخال رقم ايصال الدفع')

        # قائمة الأرقام التي يمكن تكرارها
        exceptions = ['111', '222', '333']

        # تحقق مما إذا كان رقم الإيصال موجود بالفعل
        existing_records = BookDistribution.objects.filter(
            receipt_number=receipt_number,
        ).exclude(receipt_number__in=exceptions)

        # إذا كان هناك سجلات موجودة
        if existing_records.exists():
            raise ValidationError('رقم الإيصال موجود بالفعل')

        return receipt_number

    def clean_student(self):
        student = self.cleaned_data.get('student')
        if not student:
            raise forms.ValidationError('يرجى تحديد الطالب')
        return student

    class Meta:
        model = BookDistribution
        fields = ['search_student', 'student', 'stage', 'class_level', 'section', 'receipt_number', 'books', 'notebooks', 'booklets', 'recipient_name', 'distribution_status', 'delivery_date']


#################################################################################################################################

from .models import StockReport



class StockReportForm(forms.ModelForm):
    report_name = forms.ChoiceField(choices=[], required=False, label='اسم التقرير')
    class_levels = forms.ModelChoiceField(queryset=ClassLevel.objects.all(), required=True, label='الصف الدراسي')

    class Meta:
        model = StockReport
        fields = ['stage', 'class_levels', 'academic_year', 'term']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    # تعيين اختيارات اسم التقرير
        self.fields['report_name'].choices = self.get_report_choices()
  
    def get_report_choices(self):
        # تحديد اسماء التقارير المتاحة
        available_reports = [
            ('total_books_received', 'إجمالي الكتب الواردة'),
            ('total_books_issued', 'إجمالي الكتب المصروفة'),
            ('total_notebooks_assigned', 'إجمالي الكراسات المخصصة'),
            ('total_notebooks_issued', 'إجمالي الكراسات المصروفة'),
            ('total_notebooks_received', 'إجمالي الكراسات الواردة'),
            ('total_notebooks_available', 'الكمية الحالية للكراسات'),
            ('total_booklets_received', 'إجمالي البوكليتات الواردة'),
            ('total_booklets_issued', 'إجمالي البوكليتات المصروفة'),
            ('total_supplies_received', 'إجمالي الأدوات المدرسية الواردة'),
            ('total_supplies_issued', 'إجمالي الأدوات المدرسية المصروفة'),
            ('total_students', 'عدد الطلاب')
        
        ]
        return available_reports
        

