from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import Profile, Question, Answer, Tag, Like
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect, reverse
from random import choice


# Create your views here.
def paginate(request, requested_list):
    paginator = Paginator(requested_list, 5)
    page = request.GET.get('page')
    return paginator.get_page(page)


def ask(request):
    return render(request, 'app/ask.html', {})


def hot(request):
    questions = Question.objects.get_hot_questions()
    pages = paginate(request, questions)
    return render(request, 'app/index.html', {
        'questions': pages,
        'pages': pages,
    })


def new(request):
    questions = Question.objects.get_new_questions()
    pages = paginate(request, questions)
    return render(request, 'app/index.html', {
        'questions': pages,
        'pages': pages,
    })


def index(request, tag):
    questions = Question.objects.get_questions_by_tag(tag)
    pages = paginate(request, questions)
    return render(request, 'app/index.html', {
        'questions': pages,
        'pages': pages,
    })


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            next_to = request.POST.get('next', '/new/')
            return redirect(next_to)
        else:
            return render(request, 'app/login.html', {'error_message': 'Invalid login or password'})
    return render(request, 'app/login.html', {})


def question(request, question_id):
    q = Question.objects.get_question(question_id)
    pages = paginate(request, q['answers'])
    return render(request, 'app/question.html', {
        'question': q,
        'pages': pages,
    })


def settings(request, user_id):
    return render(request, 'app/settings.html', {})


def signup(request):
    return render(request, 'app/signup.html', {})
