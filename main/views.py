from django.shortcuts import render, get_object_or_404, redirect
from .models import Service, Testimonial, ContactMessage, Exam, Question, Choice, UserResponse, Category
from .forms import CategoryForm, ExamForm, ChoiceForm, QuestionForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

# Driving School Views
def home(request):
    testimonials = Testimonial.objects.all()[:3]
    return render(request, 'main/home.html', {'testimonials': testimonials})

def about(request):
    return render(request, 'main/about.html')

def services(request):
    services = Service.objects.all()
    return render(request, 'main/services.html', {'services': services})

def contact(request):
    return render(request, 'main/contact.html')




# new page def
def ques(request):
    return render(request, 'main/ques.html')




# Exam Section Views
def exam_list(request):
    exams = Exam.objects.all()
    categories = Category.objects.all()  # Get all categories
    return render(request, 'main/exam_list.html', {'exams': exams, 'categories': categories})


from django.shortcuts import get_object_or_404, render
from .models import Exam, Question, Choice, UserResponse

def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == 'POST':
        correct_count = 0
        user_responses = []

        for question in exam.questions.all():
            selected_choice_id = request.POST.get(f'question_{question.id}')
            if selected_choice_id:  # Ensure a choice was selected
                try:
                    selected_choice = Choice.objects.get(id=selected_choice_id, question=question)
                    is_correct = selected_choice.is_correct

                    # Store the response
                    user_response = UserResponse.objects.create(
                        question=question,
                        selected_choice=selected_choice,
                        is_correct=is_correct
                    )

                    user_responses.append({
                        'question': question,
                        'selected_choice': selected_choice,
                        'is_correct': is_correct,
                        'correct_choice': question.choices.filter(is_correct=True).first()  # Get correct choice
                    })

                    if is_correct:
                        correct_count += 1
                except Choice.DoesNotExist:
                    continue

        total_questions = exam.questions.count()
        score = (correct_count / total_questions) * 100 if total_questions > 0 else 0

        return render(request, 'main/exam_result.html', {
            'exam': exam,
            'score': score,
            'total_questions': total_questions,
            'correct_count': correct_count,
            'user_responses': user_responses  # Pass user responses and correct answers to the template
        })

    questions = exam.questions.all()
    return render(request, 'main/exam_detail.html', {'exam': exam, 'questions': questions})

# Category view
@user_passes_test(lambda u: u.is_superuser)
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('control_panel')
    return render(request, 'main/add_category.html')

@user_passes_test(lambda u: u.is_superuser)
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.save()
        return redirect('control_panel')
    return render(request, 'main/edit_category.html', {'category': category})

@user_passes_test(lambda u: u.is_superuser)
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('control_panel')


# Exam view
@user_passes_test(lambda u: u.is_superuser)
def add_exam(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.category = category
            exam.save()
            return redirect('exam_list')  # Redirect to the exam list after adding
    else:
        form = ExamForm()
    return render(request, 'main/add_exam.html', {'form': form, 'category': category})

# Question view
@user_passes_test(lambda u: u.is_superuser)
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = QuestionForm()
    return render(request, 'main/add_question.html', {'form': form})

# Choice view
def add_choice(request):
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ChoiceForm()
    return render(request, 'main/add_choice.html', {'form': form})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'main/category_list.html', {'categories': categories})



# Restrict access to superusers (admin)
@user_passes_test(lambda u: u.is_superuser)
def control_panel(request):
    return render(request, 'main/control_panel.html')

@user_passes_test(lambda u: u.is_superuser)
def edit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == 'POST':
        exam.title = request.POST.get('title')
        exam.description = request.POST.get('description')
        exam.save()
        return redirect('control_panel')
    
    return render(request, 'main/edit_exam.html', {'exam': exam})

@user_passes_test(lambda u: u.is_superuser)
def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == 'POST':
        exam.delete()
        return redirect('control_panel')
    
    return render(request, 'main/delete_exam.html', {'exam': exam})

@user_passes_test(lambda u: u.is_superuser)
def add_question(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        Question.objects.create(question_text=question_text, exam=exam)
        return redirect('control_panel')
    
    return render(request, 'main/add_question.html', {'exam': exam})

@user_passes_test(lambda u: u.is_superuser)
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        question.question_text = request.POST.get('question_text')
        question.save()
        return redirect('control_panel')
    
    return render(request, 'main/edit_question.html', {'question': question})

@user_passes_test(lambda u: u.is_superuser)
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        question.delete()
        return redirect('control_panel')
    
    return render(request, 'main/delete_question.html', {'question': question})


def category_exams(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    exams = category.exams.all()  # Use the related_name 'exams' to fetch exams in the category
    return render(request, 'main/category_exams.html', {'category': category, 'exams': exams})
