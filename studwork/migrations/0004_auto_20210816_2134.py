# Generated by Django 3.2.6 on 2021-08-16 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studwork', '0003_auto_20210816_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='lesson_themes',
            field=models.ManyToManyField(related_query_name='lesson_themes', to='studwork.LessonTheme', verbose_name='Темы'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='test',
            field=models.ManyToManyField(related_query_name='lesson_test', to='studwork.Test', verbose_name='Тест'),
        ),
    ]
