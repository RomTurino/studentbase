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
    contracts = Contract.objects.filter(course=title)
    students = Student.objects.filter(id__in=contracts)
    content = {'courses': courses,
               'course': course,
               'students': students}
    return render(request, 'studbase/all_courses.html', content)


def one_student(request, id):
    student = Student.objects.get(id=id)
    contracts = Contract.objects.filter(student=id)
    parent = Parent.objects.get(id__in=contracts)
    lessons = Lesson.objects.filter(pk__in=contracts)
    lesson_themes = LessonTheme.objects.filter(pk__in=lessons)
    tests = Test.objects.filter(lesson_test__in=lessons)
    content = dict(student=student,
                   parent=parent,
                   contracts=contracts,
                   lessons=lesson_themes,
                   tests=tests)
    return render(request, 'studbase/student_detail.html', content)


def one_parent(request, id):
    parent = Parent.objects.get(id=id)

    contracts = Contract.objects.filter(parent=id)
    children = Student.objects.filter(id__in=contracts)
    print(contracts)
    content = dict(parent=parent,
                   children=children)
    return render(request, 'studbase/parent_detail.html', content)


def one_teacher(request, id):
    teacher = Teacher.objects.get(id=id)
    contracts = Contract.objects.filter(teacher=id)
    students = Student.objects.filter(id__in=contracts)
    subordinates= Teacher.objects.filter(id=id)
    if teacher.curator == teacher:
        heading = 'Подчиненные'
    else:
        heading = 'Куратор'
    content = dict(teacher=teacher,
                   students=students,
                   heading=heading,
                   subordinates=subordinates)
    return render(request, 'studbase/teacher_detail.html', content)
