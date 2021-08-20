from django.urls import path
from studwork import views

urlpatterns = [
    path('students/', views.Students.as_view(), name='students'),
    path('search/', views.SearchStudents.as_view(), name='search'),
    path('students_reverse/', views.SortStudents.as_view(), name='reverse')
]
