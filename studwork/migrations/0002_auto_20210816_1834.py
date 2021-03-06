# Generated by Django 3.2.6 on 2021-08-16 15:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('studwork', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contract',
            options={'ordering': ['contract_date'], 'verbose_name': 'Договор', 'verbose_name_plural': 'Договора'},
        ),
        migrations.AlterModelOptions(
            name='courseplan',
            options={'ordering': ['title'], 'verbose_name': 'План курса', 'verbose_name_plural': 'Планы курса'},
        ),
        migrations.AlterModelOptions(
            name='lessontheme',
            options={'ordering': ['content'], 'verbose_name': 'Тема урока', 'verbose_name_plural': 'Темы урока'},
        ),
        migrations.AlterModelOptions(
            name='parent',
            options={'ordering': ['name'], 'verbose_name': 'Родитель', 'verbose_name_plural': 'Родители'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['name'], 'verbose_name': 'Ученик', 'verbose_name_plural': 'Ученики'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'ordering': ['surname'], 'verbose_name': 'Учитель', 'verbose_name_plural': 'Учители'},
        ),
        migrations.AlterModelOptions(
            name='test',
            options={'ordering': ['code'], 'verbose_name': 'Тест', 'verbose_name_plural': 'Тесты'},
        ),
        migrations.AlterField(
            model_name='lesson',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='curator',
            field=models.ForeignKey(blank=True, max_length=150, null=True, on_delete=django.db.models.deletion.SET_NULL, to='studwork.teacher', verbose_name='Куратор'),
        ),
        migrations.AlterField(
            model_name='test',
            name='grade',
            field=models.IntegerField(blank=True, null=True, verbose_name='Оценка'),
        ),
    ]
