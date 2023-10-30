from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Course, Lesson
from .forms import LessonForm
from django.contrib import messages
from .models import Quiz, Question, Choice

def home(request):
    courses = Course.objects.all()
    return render(request, 'home.html', {'courses': courses})
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Đăng ký thành công!')  # Thêm thông báo thành công
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    course = lesson.course
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)  # Pass the instance for updating
        if form.is_valid():
            form.save()
            messages.success(request, 'Lesson updated successfully.')
            return redirect('lesson_detail', lesson_id=lesson_id)
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'lesson_detail.html', {
        'lesson': lesson,
        'form': form,
        'course': course,
    })
def course_lessons(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lessons = course.lesson_set.all()  # Lấy danh sách bài học của khóa học
    return render(request, 'course_lessons.html', {'course': course, 'lessons': lessons})

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

def quiz_detail(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'quiz_detail.html', context)

def quiz_answer(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        score = 0
        total_questions = 0

        for question in quiz.question_set.all():
            selected_choice_id = request.POST.get(f'question_{question.id}', None)
            if selected_choice_id:
                selected_choice = question.choice_set.get(id=int(selected_choice_id))
                if selected_choice.is_correct:
                    score += 1
            total_questions += 1

        percentage_score = (score / total_questions) * 100

        return render(request, 'quiz_result.html', {'quiz': quiz, 'score': score, 'total_questions': total_questions, 'percentage_score': percentage_score})

    else:
        return redirect('quiz_detail', quiz_id=quiz_id)