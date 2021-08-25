from django.shortcuts import render
from .models import *
from .filters import StudentFilter


def all_students(request):
    students = Student.objects.all()
    myFilter = StudentFilter(request.GET, queryset=students)
    students = myFilter.qs
    content = {'students': students, 'myFilter': myFilter}
    return render(request, 'studbase/all_students.html', content)


def all_courses(request):
    courses = CoursePlan.objects.all()
    students = Student.objects.all()
    content = {'courses': courses, 'students': students}
    return render(request, 'studbase/all_courses.html', content)


def one_course(request, title):
    course = CoursePlan.objects.get(title=title)
    courses = CoursePlan.objects.all()
    contracts = Contract.objects.filter(course = title)
    students = Student.objects.filter(id__in = contracts)
    content = {'courses': courses,
               'course': course,
               'students': students}
    return render(request, 'studbase/all_courses.html', content)
