# Generated by Django 3.2.6 on 2021-08-16 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studwork', '0002_auto_20210816_1834'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['lesson_date', 'lesson_type'], 'verbose_name': 'Урок', 'verbose_name_plural': 'Уроки'},
        ),
        migrations.AlterField(
            model_name='lesson',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
