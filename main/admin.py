from django.contrib import admin
# Register your models here.
from django.contrib import admin
from .models import Service, Testimonial, ContactMessage, Exam, Question, Choice, UserResponse
from .models import Category, Exam, Question, Choice

from django.contrib import admin
from .models import Exam, Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'question_text')
    inlines = [ChoiceInline]
    fields = ('exam', 'question_text', 'question_image')  # Show image field in admin

class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'category')

admin.site.register(Category)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Service)
admin.site.register(Testimonial)
admin.site.register(ContactMessage)
admin.site.register(UserResponse)
