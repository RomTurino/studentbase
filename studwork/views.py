from django.db.models import QuerySet, Q
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
        queryset = super().get_queryset()
        age_min = Q(age__gte=self.request.GET.get('min') if self.request.GET.get('min') else 0)
        age_max = Q(age__lte=self.request.GET.get('max') if self.request.GET.get('max') else 100)
        search =  Q(name__icontains=self.request.GET.get('searching') if self.request.GET.get('searching') else "")
        up_or_down = 'name' if self.request.GET.get('up') else '-name'
        queryset = queryset.filter(age_min&age_max&search).order_by(up_or_down)
        #if self.request.GET.get('min') is not None:
        # age_min = self.request.GET.get('min')
        # age_max = self.request.GET.get('max')
        # queryset = queryset.filter(age__gte=age_min if age_min else 0).filter(age__lte=age_max if age_max else 100)

        # if self.request.GET.get('searching') is not None:
        #     queryset = queryset.filter(name__icontains=self.request.GET.get('searching'))
        # if self.request.GET.get('up') or self.request.GET.get('up') is None:
        #     queryset = queryset.order_by('name')
        # if self.request.GET.get('down'):
        #     queryset = queryset.order_by('-name')
        return queryset

# def students(request):
#     queryset = Student.objects.all()
#     if request.GET.get('min'):

class SearchStudents(ListView):
    template_name = 'studbase/all_students.html'
    context_object_name = 'students'

    def get_queryset(self):
        global queryset
        queryset=queryset.filter(name__icontains=self.request.GET.get('searching').capitalize())
        return queryset


class SortStudents(ListView):
    template_name = 'studbase/all_students.html'
    context_object_name = 'students'

    def get_queryset(self):
        global queryset
        if self.request.GET.get('up'):
            queryset = queryset.order_by('name')
            return queryset
        if self.request.GET.get('down'):
            queryset = queryset.order_by('-name')
            return queryset
        if self.request.GET.get('min') is not None:
            age_min = self.request.GET.get('min')
            age_max = self.request.GET.get('max')
            return queryset.filter(age__gte=age_min).filter(age__lte=age_max)
