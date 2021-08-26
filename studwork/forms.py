from django import forms
from .models import Lesson, LessonTheme


class LessonForm(forms.ModelForm):
    lesson_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    lesson_date = forms.DateField(widget=forms.SelectDateWidget(attrs={'type': 'date'}))

    class Meta:
        model = Lesson
        exclude = ['objects']
        widget = {
            'is_done': forms.BooleanField()
        }
