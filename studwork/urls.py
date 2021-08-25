from django.urls import path
from studwork import views

urlpatterns = [
    path('students/', views.all_students, name='students'),
    path('courses/', views.all_courses, name='courses'),
    path('course/<str:title>', views.one_course, name='course'),


]
