from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.all_students, name='students'),
    path('courses/', views.all_courses, name='courses'),
    path('course/<str:title>', views.one_course, name='course'),
    path('student/<int:id>', views.one_student, name='stud_detail'),
    path('parent/<int:id>', views.one_parent, name='parent'),
    path('teacher/<int:id>', views.one_teacher, name='teacher')

]
