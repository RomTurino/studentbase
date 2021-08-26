from django.core.cache import caches, cache
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page

from .forms import LessonForm
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

@cache_page(60 * 5)
def one_student(request, id):
    print(caches)
    student = Student.objects.get(id=id)
    contracts = Contract.objects.filter(student=id)
    parent = Parent.objects.get(id__in=contracts)
    lessons = Lesson.objects.filter(pk__in=contracts)
    lesson_themes = LessonTheme.objects.filter(pk__in=lessons)
    tests = Test.objects.filter(lesson_test__in=lessons)
    lesson_field_names = "Тип урока, Дата проведения, Время урока, Тема, Проведен, Количество правильных ответов".split(
        ', ')

    content = dict(student=student,
                   parent=parent,
                   contracts=contracts,
                   lessons=lessons.order_by('is_done'),
                   lesson_themes=lesson_themes,
                   tests=tests,
                   lesson_field_names=lesson_field_names)
    cache.set('content', content)
    print(cache['content'])
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
    subordinates = Teacher.objects.filter(id=id)
    if teacher.curator == teacher:
        heading = 'Подчиненные'
    else:
        heading = 'Куратор'
    content = dict(teacher=teacher,
                   students=students,
                   heading=heading,
                   subordinates=subordinates)
    return render(request, 'studbase/teacher_detail.html', content)


def one_lesson(request, id):
    if request.method == 'GET':
        print('сейчас гет')
        lesson = Lesson.objects.filter(id=id)
        lesson_theme = LessonTheme.objects.filter(pk__in=lesson).first()
        form = LessonForm(instance=lesson.first())
        contracts = Contract.objects.filter(lessons=id)
        student = Student.objects.filter(id__in=contracts).first()
        content = dict(form=form,
                       lesson=lesson_theme,
                       student=student)
        return render(request, 'studbase/change_detail.html', content)
    else:
        print(request.method)
        lesson = get_object_or_404(Lesson, pk=id)
        form = LessonForm(request.POST, instance=lesson)
        try:
            print('try')
            form.save()
        except ValueError:
            print('valuev')
            lesson = Lesson.objects.update(form)
        finally:
            return redirect('stud_detail', id=id)
        # lesson = Lesson.objects.get(id=id)
        # form = LessonForm(request.POST, instance=lesson)
        # if form.is_valid():
        #     form.save()
        # return redirect('stud_detail', id=id)


def create_lesson(request, id):
    if request.method == 'GET':
        form = LessonForm()
        return render(request, 'studbase/change_detail.html', {'form': form})
    else:
        form = LessonForm(request.POST)
        lesson = Lesson.objects.filter(pk=id)
        contract = Contract.objects.get(lessons__in=lesson)
        try:
            print('try')
            form.save()
            contract.lessons.set(form)
        except ValueError:
            pass

        return redirect('stud_detail', id=id)


        # contract = Contract.objects.get(lessons=id)
        # if form.is_valid():
        #     data = form.cleaned_data
        #     lesson_type = data.get('lesson_type')
        #     lesson_theme = data.get('lesson_theme')
        #     test = data.get('test')
        #     lesson_time = data.get('lesson_time')
        #     lesson_date = data.get('lesson_date')
        #     is_done = data.get('is_done')
        #     right_answers = data.get('right_answers')
        #     lesson = Lesson.objects.create(lesson_type=lesson_type,
        #                                    lesson_theme=lesson_theme,
        #                                    test=test,
        #                                    lesson_time=lesson_time,
        #                                    lesson_date=lesson_date,
        #                                    is_done=is_done,
        #                                    right_answers=right_answers)
        #     contract.lessons.add(lesson)
        #
        # return redirect('stud_detail', id=id)
