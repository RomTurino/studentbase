from django.contrib import admin
from .models import *




class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'course',
                    'teacher', 'parent', 'student',
                    'count_paid_lessons', 'contract_date')
    list_display_links = ('course', 'teacher', 'parent',
                          'student')
    search_fields = ('course', 'teacher', 'parent',
                     'student')


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'curator', 'specialization')
    list_display_links = ('name', 'surname')
    search_fields = ('name', 'surname', 'curator', 'specialization')


class ParentAdmin(admin.ModelAdmin):
    list_display = ('name', 'administrator')
    search_fields = ('name', 'administrator')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')
    search_fields = ('name', 'age')


class LessonAdmin(admin.ModelAdmin):

    list_display = ('lesson_date', 'lesson_type', 'lesson_time',
                    'is_done', 'right_answers')
    list_display_links = ('lesson_date', 'lesson_type')
    search_fields = ('lesson_date', 'lesson_type', 'is_done')


class TestAdmin(admin.ModelAdmin):
    list_display = ('code', 'content', 'question_count', 'grade')
    list_display_links = ('code', 'content')
    search_fields = ('code', 'content')


class LessonThemeAdmin(admin.ModelAdmin):
    list_display = ('code', 'content', 'grade')
    list_display_links = ('code', 'content')
    search_fields = ('code', 'content', 'grade')


class CoursePlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_grade')
    search_fields = ('title', 'course_grade')


admin.site.register(Contract, ContractAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Parent, ParentAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Lesson)
admin.site.register(Test, TestAdmin)
admin.site.register(CoursePlan, CoursePlanAdmin)
admin.site.register(LessonTheme, LessonThemeAdmin)
