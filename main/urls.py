from django.urls import path
from main.views import home, about, services,contact,exam_list,exam_detail, add_category, add_choice,add_exam,add_question, category_exams
from main.views import category_list 
from .views import control_panel, add_category, edit_category, delete_category, add_exam, edit_exam, delete_exam, add_question, edit_question, delete_question

urlpatterns = [
    path('', home , name='home'),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
    path('contact/', contact, name='contact'),
    path('exams/', exam_list, name='exam_list'),
    path('exams/<int:exam_id>/', exam_detail, name='exam_detail'), 
    path('categories/', category_list, name='category_list'),  # Add this line for category list
    path('question/<int:question_id>/choice/add/', add_choice, name='add_choice'),


    path('control-panel/', control_panel, name='control_panel'),
    path('category/add/', add_category, name='add_category'),
    path('category/edit/<int:category_id>/', edit_category, name='edit_category'),
    path('category/delete/<int:category_id>/', delete_category, name='delete_category'),
    
    path('category/<int:category_id>/exam/add/', add_exam, name='add_exam'),
    path('exam/edit/<int:exam_id>/', edit_exam, name='edit_exam'),
    path('exam/delete/<int:exam_id>/', delete_exam, name='delete_exam'),
    
    path('exam/<int:exam_id>/question/add/', add_question, name='add_question'),
    path('question/edit/<int:question_id>/', edit_question, name='edit_question'),
    path('question/delete/<int:question_id>/', delete_question, name='delete_question'),
    path('category/<int:category_id>/exams/', category_exams, name='category_exams'),  # New URL for viewing exams in a category
]
