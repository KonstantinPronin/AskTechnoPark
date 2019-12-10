from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import Profile, Question, Answer, Tag, Like
from django.contrib.auth.models import User
from random import choice


# Create your views here.
def paginate(request, requested_list):
    paginator = Paginator(requested_list, 5)
    page = request.GET.get('page')
    return paginator.get_page(page)


def ask(request):
    # remove all()
    users = Profile.objects.all()
    return render(request, 'app/ask.html', {'user': choice(users)})


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


def login(request):
    return render(request, 'app/login.html', {'user': {}})


def question(request, question_id):
    q = Question.objects.get_question(question_id)
    pages = paginate(request, q['answers'])
    return render(request, 'app/question.html', {
        'question': q,
        'user': q['question'].author,
        'pages': pages,
    })


def settings(request, user_id):
    # remove all()
    users = Profile.objects.all()
    return render(request, 'app/settings.html', {'user': choice(users)})


def signup(request):
    return render(request, 'app/signup.html', {'user': {}})
