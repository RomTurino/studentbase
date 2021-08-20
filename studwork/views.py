from django.shortcuts import render, redirect
from django.urls import reverse, NoReverseMatch
from django.views import View
from django.views.generic import ListView

from .models import *




class Students(ListView):
    model = Student
    template_name = 'studbase/all_students.html'
    context_object_name = 'students'
    def get_queryset(self):
        if self.request.GET.get('min') is not None:
            age_min = self.request.GET.get('min')
            age_max = self.request.GET.get('max')
            return Student.objects.filter(age__gte = age_min).filter(age__lte = age_max)
        else:
            return Student.objects.all()



class SearchStudents(ListView):
    template_name = 'studbase/all_students.html'
    context_object_name = 'students'

    def get_queryset(self):
        return Student.objects.filter(name__icontains=self.request.GET.get('searching').capitalize())

class SortStudents(ListView):

    template_name = 'studbase/all_students.html'
    context_object_name = 'students'

    def get_queryset(self):
        if self.request.GET.get('up'):
            return Student.objects.all()
        if self.request.GET.get('down'):
            return Student.objects.all().order_by('-name')
        if self.request.GET.get('min') is not None:
            age_min = self.request.GET.get('min')
            age_max = self.request.GET.get('max')
            return Student.objects.filter(age__gte = age_min).filter(age__lte = age_max)



