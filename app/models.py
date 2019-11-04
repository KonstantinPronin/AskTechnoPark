from django.db import models
from django.conf import settings


# Create your models here.
def get_answers_and_tags_for_question(question):
    answers = question.get_answers()
    tags = question.get_tags()
    return {'question': question,
            'answers': answers,
            'tags': tags}


class QuestionManager(models.Manager):
    def get_hot_questions(self):
        questions = self.order_by('-like')
        result = []
        for question in questions:
            result.append(get_answers_and_tags_for_question(question))
        return result

    def get_new_questions(self):
        questions = self.order_by('-id')
        result = []
        for question in questions:
            result.append(get_answers_and_tags_for_question(question))
        return result

    def get_questions_by_tag(self, tag):
        if tag == 'hot':
            return self.get_hot_questions()

        if tag == 'new':
            return self.get_new_questions()

        questions_id = Tag.objects.get_questions_id_by_tag(tag)
        questions = self.filter(pk__in=questions_id)
        result = []
        for question in questions:
            result.append(get_answers_and_tags_for_question(question))
        return result

    def get_question(self, question_id):
        question = self.get(pk=question_id)
        return get_answers_and_tags_for_question(question)


class TagManager(models.Manager):
    def get_questions_id_by_tag(self, tag):
        return self.filter(name=tag).values_list('question', flat=True)


class LikeManager(models.Manager):
    def create(self, *args, **kwargs):
        if 'question' in kwargs:
            Question.objects.get(pk=kwargs['question'].pk).increment_likes()
        if 'answer' in kwargs:
            Answer.objects.get(pk=kwargs['answer'].pk).increment_likes()
        return super().create(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100, null=True)
    image = models.FilePathField(null=True)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    name = models.CharField(max_length=200)
    body = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    objects = QuestionManager()

    def increment_likes(self):
        self.likes = self.likes + 1
        self.save()

    def get_answers(self):
        return Answer.objects.filter(question=self.pk)

    def get_tags(self):
        return Tag.objects.filter(question=self.pk)

    def __str__(self):
        return self.name


class Answer(models.Model):
    body = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def increment_likes(self):
        self.likes = self.likes + 1
        self.save()

    def __str__(self):
        return self.body


class Tag(models.Model):
    name = models.CharField(max_length=50)
    question = models.ManyToManyField(Question)
    objects = TagManager()

    def __str__(self):
        return self.name


class Like(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    objects = LikeManager()
