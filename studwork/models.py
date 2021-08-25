import uuid

from django.db import models


class Contract(models.Model):
    contract_number = models.IntegerField(verbose_name='Номер договора',
                                          primary_key=True)
    teacher = models.OneToOneField('Teacher', on_delete=models.CASCADE,
                                   related_query_name='teacher',
                                   verbose_name='Преподаватель')
    parent = models.OneToOneField('Parent', on_delete=models.CASCADE,
                                  related_query_name='parent',
                                  verbose_name='Родитель')
    student = models.ForeignKey('Student', on_delete=models.CASCADE,
                                related_query_name='student',
                                verbose_name='Ученик')
    lessons = models.ManyToManyField('Lesson', related_query_name='lesson',
                                     verbose_name='Уроки')
    count_paid_lessons = models.IntegerField(verbose_name='Количество купленных уроков')
    contract_date = models.DateTimeField(verbose_name='Дата заключения',
                                         auto_now_add=True)
    course = models.ForeignKey('CoursePlan', on_delete=models.CASCADE,
                               related_query_name='course',
                               verbose_name='Курс')

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Договора'
        verbose_name = 'Договор'
        ordering = ['contract_date']

    def __str__(self):
        return f'{self.contract_number}. {self.teacher} - {self.parent}'


class Teacher(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    surname = models.CharField(max_length=150, verbose_name='Фамилия')
    curator = models.ForeignKey('self', on_delete=models.SET_NULL,
                                max_length=150, verbose_name='Куратор',
                                null=True, blank=True)
    specialization = models.CharField(max_length=150,
                                      verbose_name='Специализация')

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Учителя'
        verbose_name = 'Учитель'
        ordering = ['surname']

    def __str__(self):
        return f'{self.surname} {self.name[:1]}.'


class Parent(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    administrator = models.OneToOneField(Teacher, on_delete=models.CASCADE,
                                         verbose_name='Администратор')

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Родители'
        verbose_name = 'Родитель'
        ordering = ['name']

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    age = models.IntegerField(verbose_name='Возраст')
    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Ученики'
        verbose_name = 'Ученик'
        ordering = ['id']

    def __str__(self):
        return self.name


class Lesson(models.Model):
    KINDS = (
        ('s', 'Обычный'),
        ('k', 'Контрольный')
    )
    lesson_type = models.CharField(max_length=1, choices=KINDS, default='s',
                                   verbose_name='Обычный/контрольный')
    lesson_themes = models.ManyToManyField('LessonTheme', related_query_name='lesson_themes',
                                           verbose_name='Темы')
    test = models.ManyToManyField('Test', related_query_name='lesson_test',
                                  verbose_name='Тест')
    lesson_time = models.TimeField(verbose_name='Время урока')
    lesson_date = models.DateField(verbose_name="Дата урока")
    is_done = models.BooleanField(verbose_name="Проведен")
    right_answers = models.IntegerField(verbose_name="Количество правильных ответов")
    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Уроки'
        verbose_name = 'Урок'
        ordering = ['lesson_date', 'lesson_type']

    def __str__(self):
        if self.lesson_type == 's':
            return f'Обычный, {self.lesson_date} {self.lesson_time}'
        else:
            return f'Контрольный, {self.lesson_date} {self.lesson_time}'


class Test(models.Model):
    code = models.IntegerField(verbose_name='Код теста', primary_key=True)
    question_count = models.IntegerField(verbose_name='количество вопросов')
    content = models.TextField(verbose_name='Контент')
    grade = models.IntegerField(verbose_name='Оценка', blank=True, null=True)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Тесты'
        verbose_name = 'Тест'
        ordering = ['code']

    def __str__(self):
        return f'{self.code}'


class CoursePlan(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название курса',
                             primary_key=True)
    course_grade = models.IntegerField(verbose_name='Оценка')
    test = models.ManyToManyField(Test, related_query_name='plan_to_test',
                                  verbose_name='Тест')
    themes = models.ManyToManyField('LessonTheme', related_query_name='themes',
                                    verbose_name='Темы')

    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Планы курса'
        verbose_name = 'План курса'
        ordering = ['title']

    def __str__(self):
        return self.title


class LessonTheme(models.Model):
    code = models.IntegerField(verbose_name='Код урока', primary_key=True)
    content = models.TextField(verbose_name='Содержание')
    grade = models.IntegerField(verbose_name='Оценка темы')
    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Темы урока'
        verbose_name = 'Тема урока'
        ordering = ['content']

    def __str__(self):
        return f'{self.code}. {self.content[:10]}'
