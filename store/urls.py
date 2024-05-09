from django import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views


app_name = 'store'
urlpatterns = [
    path('list/', views.list, name='list'),
    path('home/', views.home, name='home'),
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    path('allstudent/', views.allstudent, name='allstudent'),
    path('add/', add_student, name='add_student'),
    path('import/', import_students, name='import_students'),
    path('export/', export_students, name='export_students'),
    path('students/', studentListView.as_view(), name='student_list'),
    path('export_Student_excel/', export_Student_excel, name='export_Student_excel'),
    ##################################################################
    path('bookstore/', views.bookstore, name='bookstore'),
    path('add_book/', add_book, name='add_book'),
    path('book_list/', BookListView.as_view(), name='book_list'),
    path('add_notebook_type/', add_notebook_type, name='add_notebook_type'),
    path('add_notebook_assignment/', add_notebook_assignment, name='add_notebook_assignment'),
    path('add_school_booklet/', views.add_school_booklet, name='add_school_booklet'),
    path('get_class_levels/', views.get_class_levels, name='get_class_levels'),
    path('get_class_student/', views.get_class_student, name='get_class_student'),
    path('add_school_supplies/', views.add_school_supplies, name='add_school_supplies'),
    ################################################################################
    path('book_distribution/', BookDistributionCreateView.as_view(), name='book_distribution'),
    path('search_student/', views.search_student, name='search_student'),
    path('get_selected_student/', views.get_selected_student, name='get_selected_student'),  # الإضافة الجديدة
    path('get_student_info/', views.get_student_info, name='get_student_info'),
    path('get_available_books/', views.get_available_books, name='get_available_books'),
    path('get_available_notebooks/', views.get_available_notebooks, name='get_available_notebooks'),
    path('get_available_booklets/', views.get_available_booklets, name='get_available_booklets'),
    path('book-distribution/', BookDistributionListView.as_view(), name='book_distribution_list'),
    
    path('book-distribution/<int:pk>/update/', BookDistributionUpdateView.as_view(), name='book_distribution_update'),
    path('book-distribution/<int:pk>/delete/', BookDistributionDeleteView.as_view(), name='book_distribution_delete'),
    path('export_to_excel/', export_to_excel, name='export_to_excel'),

    
    


    #path('stock-report/', views.stock_report_view, name='stock_report'),
    #path('load-class-levels/', views.load_class_levels, name='load_class_levels'),
    #path('generate-report/', views.generate_report, name='generate_report'),
  




   

]




