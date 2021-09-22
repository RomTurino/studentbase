from django import forms
from .models import Lesson, LessonTheme


class LessonForm(forms.ModelForm):
    lesson_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    lesson_date = forms.DateField(widget=forms.SelectDateWidget(attrs={'type': 'date'}))
    right_answers = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0, 'max': 100}),required=False)

    class Meta:
        model = Lesson
        fields = '__all__'
        widget = {
            'is_done': forms.BooleanField()
        }
