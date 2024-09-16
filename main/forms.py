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
        fields = ['question_text', 'exam']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', 'is_correct', 'question']
