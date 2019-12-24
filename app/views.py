from django.db import IntegrityError
from django.shortcuts import render
from django.core.paginator import Paginator
from app.models import Profile, Question, Answer, Tag, Like, get_profile_by_user, get_tag_by_name
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render, redirect, reverse
from random import choice


# Create your views here.
def paginate(request, requested_list):
    paginator = Paginator(requested_list, 5)
    page = request.GET.get('page')
    return paginator.get_page(page)


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


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        rpassword = request.POST['rpassword']
        avatar = request.POST['avatar']
        if password != rpassword:
            return render(request, 'app/signup.html', {'error_message': 'Passwords do not match'})
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            Profile.objects.create(user=user, image=avatar, email=email, name=name)
        except IntegrityError:
            return render(request, 'app/signup.html', {'error_message': 'Such username already exists'})
        auth.login(request, user)
        next_to = request.POST.get('next', '/new/')
        return redirect(next_to)
    return render(request, 'app/signup.html', {})


def ask(request):
    if request.method == 'POST':
        user = request.user
        author = get_profile_by_user(user)
        name = request.POST['name']
        body = request.POST['body']
        tagname = request.POST['tag']
        q = Question.objects.create(name=name, body=body, author=author)
        tags = get_tag_by_name(tagname)
        for tag in tags:
            tag.question.set([q])
        next_to = request.POST.get('next', '/new/')
        return redirect(next_to)
    return render(request, 'app/ask.html', {})


def question(request, question_id):
    if request.method == 'POST':
        user = request.user
        author = get_profile_by_user(user)
        body = request.POST['answer']
        Answer.objects.create(body=body, author=author, question_id=question_id)
        next_to = request.POST.get('next', '/question/' + str(question_id))
        return redirect(next_to)
    q = Question.objects.get_question(question_id)
    answers = []
    for a in q['answers']:
        answers.append(a)
    pages = paginate(request, answers)
    return render(request, 'app/question.html', {
        'question': q,
        'pages': pages,
    })


def settings(request, user_id):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        name = request.POST['name']
        avatar = request.POST['avatar']
        try:
            user = request.user
            profile = Profile.objects.get(user=user)
            if username:
                user.username = username
            if email:
                profile.email = email
                user.email = email
            if name:
                profile.name = name
            if avatar:
                profile.image = avatar
            user.save()
            profile.save()
        except IntegrityError:
            return render(request, 'app/settings.html', {'error_message': 'Such username already exists'})
    return render(request, 'app/settings.html', {})
