from datetime import datetime
from turtle import pd

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, FormView
from django.views.generic.edit import CreateView
from django_filters.views import FilterView
from .Bookfilter import BookDistributionFilter
from django.views.generic import UpdateView, DeleteView
import xlsxwriter
from django.http import HttpResponse
from .BOOK_LIST import BookFilter


from .filters import StudentFilter
from .forms import (StockReportForm, StudentForm, BookDistributionForm, StudentSearchForm,
                    StudentSelectForm, SchoolBookletForm, SchoolSuppliesForm,
                    NotebookTypeForm, BookForm, NotebookAssignmentForm)
from .models import (AcademicYear, Book, BookDistribution, ClassLevel,
                     Classroom, NotebookAssignment, NotebookType, SchoolBooklet,
                     Stage, Student)


##############################################################################33
def home(request):

    return render(request, 'home.html')
def list(request):

    return render(request, 'list.html')

def Dashboard(request):

    return render(request, 'Dashboard.html')


def allstudent(request):

    return render(request, 'student.html')

def bookstore(request):

    return render(request, 'bookstore.html')
################################################################33

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تمت إضافة الطالب بنجاح.')
            return redirect('store:Dashboard')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

def import_students(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        if not excel_file.name.endswith('.xlsx'):
            messages.error(request, 'الملف يجب أن يكون بصيغة Excel (xlsx).')
            return redirect('import_students')
        
        df = pd.read_excel(excel_file, names=['name', 'national_id', 'stage', 'class_level', 'section', 'phone_number', 'academic_year'])
        
        for index, row in df.iterrows():
            try:
                section = Classroom.objects.filter(name=row['section']).first()
                if not section:
                    raise Classroom.DoesNotExist()
                stage = Stage.objects.get(stage=row['stage'])
                class_level = ClassLevel.objects.get(name=row['class_level'])
                academic_year = AcademicYear.objects.get(year=row['academic_year'])
                student = Student(
                    name=row['name'],
                    national_id=row['national_id'],
                    phone_number=row['phone_number'],  # إضافة رقم الهاتف هنا
                    stage=stage,
                    class_level=class_level,
                    section=section,
                    academic_year=academic_year
                )
                student.save()
            except Classroom.DoesNotExist:
                messages.error(request, f"الفصل '{row['section']}' غير موجود.")
            except ClassLevel.DoesNotExist:
                messages.error(request, f"الصف '{row['class_level']}' غير موجود.")
            except Stage.DoesNotExist:
                messages.error(request, f"المرحلة '{row['stage']}' غير موجود.")
            except AcademicYear.DoesNotExist:
                messages.error(request, f"السنة الدراسية '{row['academic_year']}' غير موجودة.")

        messages.success(request, 'تم استيراد الطلاب بنجاح.')
        return redirect('store:add_student')
    return render(request, 'import_students.html')

def export_students(request):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"طلاب_{timestamp}.xlsx"

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    df = pd.DataFrame(list(Student.objects.values('name', 'national_id', 'stage__stage', 'class_level__name', 'section__name','phone_number', 'academic_year__year')))
    df.columns = ['اسم الطالب', 'الرقم القومي', 'المرحلة الدراسية', 'الصف الدراسي', 'الفصل الدراسي', ' رقم الهاتف', 'السنة الدراسية']
    df.to_excel(response, index=False)

    return response
def get_class_student(request):
    stage_id = request.GET.get('stage_id')
    class_levels = ClassLevel.objects.filter(stage_id=stage_id)
    data = [{'id': class_level.id, 'name': class_level.name, 'sections': list(class_level.classroom_set.all().values('id', 'name'))} for class_level in class_levels]
    return JsonResponse(data, safe=False)

##########################################################################################################################


class studentListView(FilterView):
    model = Student
    template_name = 'Student_list.html'
    filterset_class = StudentFilter
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        name = self.request.GET.get('name')

        if name:
            queryset = queryset.filter(name=name)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['Student_list'] = page_obj
        context['filter'] = self.filterset  # استخدام self.filterset بدلاً من self.filter

        return context
 #######################################################################################################33

def export_Student_excel(request):
    # تحديد اسم الملف مع تضمين التاريخ الحالي
    filename = f"Student_list_{datetime.now().strftime('%Y-%m-%d')}.xlsx"

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # إنشاء ملف Excel وورقة عمل
    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet()

    # تحضير العناوين
    headers = [
        'ترقيم',
        'اسم الطالب',
        'المرحلة الدراسية',
        'الصف الدراسي',
        'الفصل الدراسي',
        'الرقم القومي',
        'رقم التليفون',
        ' السنة الدراسية',   
    ]

    # كتابة العناوين في الصف الأول في الملف
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # استرجاع البيانات المصفاة وكتابتها في ملف Excel
    queryset = StudentFilter(request.GET, queryset=Student.objects.all()).qs

    for row, student in enumerate(queryset, start=1):
        worksheet.write(row, 0, row)  # رقم الصف
        worksheet.write(row, 1, student.name)
        worksheet.write(row, 2, str(student.stage))
        worksheet.write(row, 3, str(student.class_level))
        worksheet.write(row, 4, str(student.section))
        worksheet.write(row, 5, student.national_id)
        worksheet.write(row, 6, student.phone_number)
        worksheet.write(row, 7, student.class_level.academic_year.year if student.class_level.academic_year else '')

    # إغلاق ملف Excel وإرسال الاستجابة
    workbook.close()
    return response

########################################################3

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:bookstore')  # اسم العرض الخاص بعرض الكتب
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})
###############################################
class BookListView(FilterView):
    filterset_class = BookFilter
    queryset = Book.objects.all()
    template_name = 'book_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['title'] = 'قائمة  الكتب '
        context['page_obj'] = page_obj
        return context
    


######################################################################################


def add_notebook_type(request):
    if request.method == 'POST':
        form = NotebookTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'تمت إضافة نوع الكراسة بنجاح.')
            return redirect('store:bookstore')
    else:
        form = NotebookTypeForm()
    return render(request, 'add_notebook_type.html', {'form': form})
#####################################################################################3


def add_notebook_assignment(request):
    if request.method == 'POST':
        form = NotebookAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            # أي عمليات أخرى بعد الحفظ بنجاح
            return redirect('store:bookstore')  # قم بتغيير هذا إلى الصفحة التي ترغب في إعادة التوجيه إليها بعد الحفظ
    else:
        form = NotebookAssignmentForm()
    return render(request, 'add_notebook_assignment.html', {'form': form})

def get_class_levels(request):
    stage_id = request.GET.get('stage_id')
    class_levels = ClassLevel.objects.filter(stage_id=stage_id).order_by('name')
    return render(request, 'class_levels_options.html', {'class_levels': class_levels})
###############################################################################################


def add_school_booklet(request):
    if request.method == 'POST':
        form = SchoolBookletForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:bookstore')
    else:
        form = SchoolBookletForm()
    return render(request, 'add_school_booklet.html', {'form': form})

def get_class_levels(request):
    stage_id = request.GET.get('stage_id')
    class_levels = ClassLevel.objects.filter(stage_id=stage_id)
    data = [{'id': class_level.id, 'name': class_level.name} for class_level in class_levels]
    return JsonResponse(data, safe=False)



###############################################################################################


def add_school_supplies(request):
    if request.method == 'POST':
        form = SchoolSuppliesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:bookstore')  # يمكن تغيير الوجهة بحسب الحاجة
    else:
        form = SchoolSuppliesForm()
    return render(request, 'add_school_supplies.html', {'form': form})
##################################################################################################################################


class BookDistributionCreateView(CreateView):
    model = BookDistribution
    form_class = BookDistributionForm
    template_name = 'book_distribution_form.html'
    success_url = reverse_lazy('store:home')

    def form_valid(self, form):
        book_distribution = form.save(commit=False)
        book_distribution.student = form.cleaned_data['student']
        book_distribution.stage = form.cleaned_data['stage']
        book_distribution.class_level = form.cleaned_data['class_level']
        book_distribution.section = form.cleaned_data['section']
        book_distribution.save()

        # Save many-to-many fields
        book_distribution.books.set(form.cleaned_data['books'])
        book_distribution.notebooks.set(form.cleaned_data['notebooks'])
        book_distribution.booklets.set(form.cleaned_data['booklets'])

        return super().form_valid(form)
        
        ###################################################

def search_student(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query:
            students = Student.objects.filter(
                Q(name__icontains=query)
            ).values('id', 'name')[:10]
            return JsonResponse({'students': list(students)}, content_type='application/json; charset=utf-8')
    return JsonResponse({'students': []})


####################################3

def get_selected_student(request):
    if request.method == 'GET' and 'student_id' in request.GET:
        student_id = request.GET.get('student_id')
        try:
            selected_student = Student.objects.get(id=student_id)
            data = {
                'id': selected_student.id,
                'name': selected_student.name,
                'stage': selected_student.stage,
                'class_level': selected_student.class_level.name,
                'section': selected_student.section.name,
            }
            
            # Print the retrieved selected student data for debugging
            print("Retrieved selected student data:", data)
            
            return JsonResponse(data)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
    return JsonResponse({})

#####################################3

# الحصول على الكتب المتاحة
def get_available_books(request):
    if request.method == 'GET' and 'student_id' in request.GET:
        student = Student.objects.get(id=request.GET.get('student_id'))
        class_level = student.class_level
        stage = student.stage
        available_books = Book.objects.filter(
            stage=stage, 
            class_level=class_level
        )
        data = []
        for book in available_books:
            book_data = {
                'id': book.id,
                'title': book.title 
            }
            data.append(book_data)
        return JsonResponse({'books': data})
    return JsonResponse({})

##########################################################################3

# الحصول على الكراسات المتاحة
def get_available_notebooks(request):
    if request.method == 'GET' and 'student_id' in request.GET:
        student = Student.objects.get(id=request.GET.get('student_id'))
        class_level = student.class_level
        stage = student.stage
        available_notebooks = NotebookAssignment.objects.filter(
            stage=stage,  
            grade=class_level
        )
        data = []
        for notebook_assignment in available_notebooks:
            notebook_data = {
                'id': notebook_assignment.notebook.id,
                'name': notebook_assignment.notebook.name
            }
            data.append(notebook_data)
        return JsonResponse({'notebooks': data})
    return JsonResponse({})

#################################################################################

# الحصول على البوكليتات المتاحة
def get_available_booklets(request):
    if request.method == 'GET' and 'student_id' in request.GET:
        student = Student.objects.get(id=request.GET.get('student_id'))
        class_level = student.class_level
        stage = student.stage
        available_booklets = SchoolBooklet.objects.filter(
            stage=stage,
            class_level=class_level  
        )
        data = []  
        for booklet in available_booklets:
            booklet_data = {
                'id': booklet.id,
                'title': booklet.title
            }
            data.append(booklet_data)
        return JsonResponse({'booklets': data})
    return JsonResponse({})

####################################3
from django.http import JsonResponse

def get_student_info(request):
    if request.method == 'GET' and 'student_id' in request.GET:
        student_id = request.GET.get('student_id')
        try:
            student = Student.objects.get(id=student_id)
            stage = student.stage.stage if student.stage else None
            class_level = student.class_level.name if student.class_level else None
            section = student.section.id if student.section else None
            data = {
                'stage': stage,
                'class_level': class_level,
                'section': section,
                
            }
            return JsonResponse(data)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
    return JsonResponse({})

#########################################################################################################


class BookDistributionUpdateView(UpdateView):
    model = BookDistribution
    fields = ['student', 'stage', 'class_level', 'section', 'receipt_number', 'books', 'notebooks', 'booklets', 'delivery_date', 'distribution_status', 'recipient_name']
    template_name = 'book_distribution_update.html'
    success_url = reverse_lazy('store:book_distribution_list')


from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect

class BookDistributionDeleteView(DeleteView):
    model = BookDistribution
    success_url = reverse_lazy('store:book_distribution_list')
    template_name = 'book_distribution_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, "تم حذف توزيع الكتب والكراسات والبوكليتات بنجاح.")
        return HttpResponseRedirect(success_url)

########################################################################################################
class BookDistributionListView(FilterView):
    filterset_class = BookDistributionFilter
    queryset = BookDistribution.objects.all()
    template_name = 'book_distribution_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['title'] = 'قائمة توزيع الكتب والكراسات والبوكليتات'
        context['page_obj'] = page_obj
        return context
    


def export_to_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="book_distribution.xlsx"'

    # إنشاء ملف Excel وورقة عمل
    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet()

    # تحضير العناوين
    headers = [
        '#',
        'اسم الطالب',
        'المرحلة الدراسية',
        'الصف الدراسي',
        'الفصل الدراسي',
        'رقم الإيصال',
        'اسم المستلم',
        'تاريخ التوزيع',
        'حالة التوزيع',
        'الكتب المسلمة',
        'الكراسات المسلمة',
        'البوكليتات المسلمة',
    ]

    # كتابة العناوين في الصف الأول في الملف
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # استرجاع البيانات المصفاة وكتابتها في ملف Excel
    queryset = BookDistributionFilter(request.GET, queryset=BookDistribution.objects.all()).qs

    for row, distribution in enumerate(queryset, start=1):
        worksheet.write(row, 0, row)  # رقم الصف
        worksheet.write(row, 1, distribution.student.name)
        worksheet.write(row, 2, str(distribution.stage))
        worksheet.write(row, 3, str(distribution.class_level))
        worksheet.write(row, 4, str(distribution.section))
        worksheet.write(row, 5, distribution.receipt_number)
        worksheet.write(row, 6, distribution.recipient_name)
        worksheet.write(row, 7, distribution.delivery_date)
        worksheet.write(row, 8, distribution.get_distribution_status_display())
        worksheet.write(row, 9, distribution.get_books_titles())
        worksheet.write(row, 10, distribution.get_notebooks_titles())
        worksheet.write(row, 11, distribution.get_booklets_titles())

    # إغلاق ملف Excel وإرسال الاستجابة
    workbook.close()
    return response




########################################################################################################

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import StockReport


def stock_report_view(request):
    form = StockReportForm()
    context = {
        'form': form
    }
    return render(request, 'stock_report.html', context)

def load_class_levels(request):
    stage_id = request.GET.get('stage')
    if stage_id:
        try:
            stage = Stage.objects.get(id=stage_id)
            class_levels = ClassLevel.objects.filter(stage=stage)
            class_levels_data = [{'id': level.id, 'name': level.name} for level in class_levels]
            return JsonResponse({'class_levels': class_levels_data})
        except Stage.DoesNotExist:
            return JsonResponse({'error': 'Invalid stage'})
    else:
        return JsonResponse({'error': 'Stage is required'})

from django.core.exceptions import ValidationError

def generate_report(request):
    if request.method == 'POST':
        form = StockReportForm(request.POST)
        if form.is_valid():
            try:
                stock_report = form.save()
            except ValidationError as e:
                return JsonResponse({'error': str(e)})
            report_name = form.cleaned_data['report_name']
            report_data = getattr(stock_report, report_name)
            html_report = render_to_string('report_template.html', {'report_data': report_data})
            return JsonResponse({'html_report': html_report})
    else:
        form = StockReportForm()
    return render(request, 'stock_report.html', {'form': form})