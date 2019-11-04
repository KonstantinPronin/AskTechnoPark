from faker import Faker
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, Like
from random import choice


class Command(BaseCommand):
    faker = Faker()

    def fill_profiles(self, cnt):
        for i in range(cnt):
            user = User(username=self.faker.name())
            user.save()
            Profile.objects.create(user=user, image='/static/img/qwerty.png', email=self.faker.name() + '@email.com',
                                   name=self.faker.name())

    def fill_questions(self, cnt):
        users = list(Profile.objects.all())
        for i in range(cnt):
            Question.objects.create(name=self.faker.name(), body=self.faker.text(), author=choice(users))

    def fill_answers(self, cnt):
        users = list(Profile.objects.all())
        questions = list(Question.objects.all())
        for i in range(cnt):
            Answer.objects.create(body=self.faker.text(), author=choice(users), question=choice(questions))

    def fill_tags(self, cnt):
        questions = list(Question.objects.all())
        for i in range(cnt):
            Tag.objects.create(name=self.faker.name()).question.set([choice(questions)])

    def fill_likes(self, cnt):
        users = list(Profile.objects.all())
        questions = list(Question.objects.all())
        answers = list(Answer.objects.all())
        for i in range(cnt):
            Like.objects.create(question=choice(questions), author=choice(users))
            Like.objects.create(answer=choice(answers), author=choice(users))

    def handle(self, *args, **options):
        cnt = 20
        self.fill_profiles(cnt)
        self.fill_questions(cnt)
        self.fill_answers(cnt)
        self.fill_tags(cnt)
        self.fill_likes(cnt)
