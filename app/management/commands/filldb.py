from faker import Faker
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
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
        users = list(Profile.objects.all().values_list('id', flat=True))
        for i in range(cnt):
            Question.objects.create(name=self.faker.name(), body=self.faker.text(), author_id=choice(users))

    def fill_answers(self, cnt):
        users = list(Profile.objects.all().values_list('id', flat=True))
        questions = list(Question.objects.all().values_list('id', flat=True))
        for i in range(cnt):
            Answer.objects.create(body=self.faker.text(), author_id=choice(users), question_id=choice(questions))

    def fill_tags(self, cnt):
        questions = list(Question.objects.all().values_list('id', flat=True))
        for i in range(cnt):
            Tag.objects.create(name=self.faker.name()).question.set([choice(questions)])

    def fill_likes(self, cnt):
        users = list(Profile.objects.all().values_list('id', flat=True))
        questions = list(Question.objects.all().values_list('id', flat=True))
        # questions = list(Question.objects.all())
        answers = list(Answer.objects.all().values_list('id', flat=True))
        # answers = list(Answer.objects.all())
        for i in range(cnt):
            Like.objects.create(object_id=choice(questions), content_type=ContentType.objects.get_for_model(Question),
                                author_id=choice(users))
            # Like.objects.create(content_object=choice(questions), author_id=choice(users))
            Like.objects.create(object_id=choice(answers), content_type=ContentType.objects.get_for_model(Answer),
                                author_id=choice(users))
            # Like.objects.create(content_object=choice(answers), author_id=choice(users))

    def create_default_user(self):
        user = User.objects.create_user('root', 'prosayfer@email.com', 'prosayfer')
        user.save()
        Profile.objects.create(user=user, image='/static/img/qwerty.png', email='prosayfer@email.com',
                               name='Konstantin')

    def handle(self, *args, **options):
        cnt = 20
        # create default user
        #self.create_default_user()

        self.fill_profiles(cnt)
        self.fill_questions(cnt)
        self.fill_answers(cnt)
        self.fill_tags(cnt)
        self.fill_likes(cnt)
