from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import StudentFilter
from .forms import LessonForm
from .models import *



cache_set = set()

@login_required
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

@login_required
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

@login_required
def one_course(request, title):
    course = CoursePlan.objects.get(title=title)
    courses = CoursePlan.objects.all()
    contracts = Contract.objects.filter(course=title)
    students = Student.objects.filter(id__in=contracts)
    content = {'courses': courses,
               'course': course,
               'students': students}
    return render(request, 'studbase/all_courses.html', content)

@login_required
@cache_page(60 * 1, key_prefix='student_page')
def one_student(request, id):
    global cache_set
    student = Student.objects.get(id=id)
    cache.set(student.id, f'{student.name}({student.age})', 60 * 1)
    cache_set.add(student.id)
    contracts = Contract.objects.filter(student=id)
    parent = Parent.objects.filter(parent__in=contracts)
    lessons = Lesson.objects.filter(lesson__in=contracts)
    lesson_themes = LessonTheme.objects.filter(lesson_themes__in=lessons)
    tests = Test.objects.filter(lesson_test__in=lessons)
    lesson_field_names = "Тип урока, Дата проведения, Время урока, Тема, Проведен, " \
                         "Количество правильных ответов, Редактирование".split(', ')
    test_field_names= "Код теста, Количество вопросов, Содержание, Оценка".split(', ')
    content = dict(student=student,
                   parent=parent,
                   contracts=contracts,
                   lessons=lessons.order_by('is_done'),
                   lesson_themes=lesson_themes,
                   tests=tests,
                   lesson_field_names=lesson_field_names,
                   test_field_names=test_field_names)

    return render(request, 'studbase/student_detail.html', content)

@login_required
def one_parent(request, id):
    parent = Parent.objects.get(id=id)
    contracts = Contract.objects.filter(parent=id)
    children = Student.objects.filter(student__in=contracts)
    content = dict(parent=parent,
                   children=children)
    return render(request, 'studbase/parent_detail.html', content)

@login_required
def one_teacher(request, id):
    teacher = Teacher.objects.get(id=id)
    contracts = Contract.objects.filter(teacher=id)
    students = Student.objects.filter(student__in=contracts)
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

@login_required
def one_lesson(request, id):
    if request.method == 'GET':
        lesson = Lesson.objects.filter(id=id)
        lesson_theme = LessonTheme.objects.filter(lesson_themes__in=lesson).first()
        form = LessonForm(instance=lesson.first())
        contracts = Contract.objects.filter(lessons__in=lesson)
        student = Student.objects.filter(student__in=contracts).first()
        content = dict(form=form,
                       lesson=lesson_theme,
                       student=student)
        return render(request, 'studbase/change_detail.html', content)
    else:
        #lesson = get_object_or_404(Lesson, pk=id)
        lesson = Lesson.objects.filter(id=id)
        contracts = Contract.objects.filter(lessons__in=lesson)
        student = Student.objects.filter(student__in=contracts).first()
        form = LessonForm(request.POST, instance=lesson.first())
        print(form)
        try:
            form.save()
            cache.clear()
        except ValueError:
            pass
        finally:
            return redirect('stud_detail', id=student.id)


@login_required
def create_lesson(request, id):
    if request.method == 'GET':
        form = LessonForm()
        return render(request, 'studbase/change_detail.html', {'form': form})
    else:
        form = LessonForm(request.POST)
        #lesson = Lesson.objects.filter(pk=id)
        contract = Contract.objects.get(student=id)
        try:
            lesson = form.save()
            contract.lessons.add(lesson)
            #lesson = Lesson.objects.last()
            #print(lesson.id)
            contract.lessons.add(lesson.id)
        except ValueError:
            pass
        cache.clear()
        return redirect('stud_detail', id=id)




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
