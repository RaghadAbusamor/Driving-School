from django import forms
from .models import Category, Exam, Question, Choice

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['title', 'description', 'category']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['exam', 'question_text', 'question_image']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['question', 'choice_text', 'choice_image', 'is_correct']

