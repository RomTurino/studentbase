import memcached_stats
from cachy.stores import memcached_store
from django.core.cache import cache, caches
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import StudentFilter
from .forms import LessonForm
from .models import *

# from memcached_stats import MemcachedStats
# mem = MemcachedStats('127.0.0.1', '11211')
# mem = mem


cache_set = set()


def all_students(request):
    students_all = Student.objects.all()
    myFilter = StudentFilter(request.GET, queryset=students_all)
    students_all = myFilter.qs
    paginator = Paginator(students_all, 20)
    page = request.GET.get('page', 1)
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    content = {'students': students, 'myFilter': myFilter, 'page': page}
    return render(request, 'studbase/all_students.html', content)


def all_courses(request):
    courses = CoursePlan.objects.all()
    students_all = Student.objects.all()
    paginator = Paginator(students_all, 20)
    page = request.GET.get('page', 1)
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

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


@cache_page(60 * 1, key_prefix='student_page')
def one_student(request, id):
    global cache_set
    student = Student.objects.get(id=id)
    cache.set(student.id, f'{student.name}({student.age})', 60 * 1)
    cache_set.add(student.id)
    contracts = Contract.objects.filter(student=id)
    parent = Parent.objects.get(id__in=contracts)
    lessons = Lesson.objects.filter(pk__in=contracts)
    print(f'договор - {contracts}')
    lesson_themes = LessonTheme.objects.filter(pk__in=lessons)
    tests = Test.objects.filter(lesson_test__in=lessons)
    lesson_field_names = "Тип урока, Дата проведения, Время урока, Тема, Проведен, Количество правильных ответов".split(
        ', ')

    content = dict(student=student,
                   parent=parent,
                   contracts=contracts,
                   lessons=lessons,
                   lesson_themes=lesson_themes,
                   tests=tests,
                   lesson_field_names=lesson_field_names)
    # print(cache.get('student'))
    # print(cache.get('student_page'))
    # key =make_template_fragment_key('student_page')
    # print(cache.get(key))
    # print(student in cache)
    # responce = render(request, 'studbase/student_detail.html', content)
    # a=patch_vary_headers(responce, ['Cookie'])
    # print(cache.get('Cookie'))
    # print(a,b)
    # print('Это точно сработает')
    return render(request, 'studbase/student_detail.html', content)


def one_parent(request, id):
    global cache_list
    parent = Parent.objects.get(id=id)
    contracts = Contract.objects.filter(parent=id)
    children = Student.objects.filter(id__in=contracts)
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
        print(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get('pk'))
        lesson = Lesson.objects.filter(pk=id)
        contract = Contract.objects.get(student=id)
        try:
            print('try')
            form.save()
            lesson = Lesson.objects.last()
            print(lesson.id)
            contract.lessons.add(lesson.id)
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


def last_students(request):
    global cache_set
    print(cache_set)
    for key in cache_set:
        if not cache.has_key(key):
            try:
                cache_set.discard(key)
            except RuntimeError:
                return render(request, 'studbase/recent_students.html',
                              {'error': 'Похоже, что-то пошло не так, обновите страницу'})
            finally:
                return render(request, 'studbase/recent_students.html',
                              {'error': 'Похоже, что-то пошло не так, обновите страницу'})
    students = Student.objects.filter(id__in=cache_set)
    content = dict(students=students)
    return render(request, 'studbase/recent_students.html', content)
