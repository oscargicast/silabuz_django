from django.db import models
from model_utils.models import TimeStampedModel


class CommonModel(TimeStampedModel):
    name = models.CharField(max_length=200)
    is_active = models.BooleanField()

    class Meta:
        abstract = True


class Course(CommonModel):
    max_capacity = models.PositiveSmallIntegerField(
        default=20,
    )
    members = models.ManyToManyField(
        'student.Student',
        through='course.Subscription',
        blank=True,
    )

    def __str__(self):
        return f'{self.id}: {self.name}'

    class Meta:
        db_table = 'course'

    @property
    def stock(self):
        return self.members.count()


class Quiz(CommonModel):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='tests',
    )
    question = models.TextField()
    # # If all the quiz options of the student
    # # were selected right, then this field is True.
    # was_succeded = models.BooleanField(
    #     null=True,
    # )

    def __str__(self):
        return f'{self.id}: {self.course.name} - {self.name}'

    class Meta:
        db_table = 'quiz'
        verbose_name_plural = "quizes"


class QuizOption(CommonModel):
    quiz = models.ForeignKey(
        'course.Quiz',
        on_delete=models.CASCADE,
        related_name='options',
    )
    is_a_right_answer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(
        default=0,
    )

    def __str__(self):
        return f'{self.id}: {self.quiz.name} - {self.name}'

    class Meta:
        db_table = 'quiz_option'


class Subscription(TimeStampedModel):
    student = models.ForeignKey(
        'student.Student',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return (
            f'{self.id}: {self.student.first_name} '
            f'subscribed to {self.course.name}'
        )

    class Meta:
        db_table = 'subscription'
        unique_together = ('student', 'course')


class QuizAnswer(TimeStampedModel):
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='quiz_answers',
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='quiz_answers',
    )
    succeeded = models.BooleanField(default=False)

    class Meta:
        db_table = 'quiz_answer'
        unique_together = ('subscription', 'quiz')

    def check_option_answers(self) -> bool:
        quiz_options = self.quiz.options.filter(
            is_a_right_answer=True
        ).values_list('id', flat=True)
        option_answers = QuizOptionAnswer.objects.filter(
            quiz_answer=self,
        ).values_list('quiz_option', flat=True)
        return (set(quiz_options) - set(option_answers)) == set()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        if is_new:
            self.succeeded = self.check_option_answers()
        # Pre save.
        super().save(*args, **kwargs)
        # Post save.


class QuizOptionAnswer(TimeStampedModel):
    quiz_answer = models.ForeignKey(
        QuizAnswer,
        on_delete=models.CASCADE,
        related_name='quiz_option_answers',
    )
    quiz_option = models.ForeignKey(
        QuizOption,
        on_delete=models.CASCADE,
        related_name='quiz_option_answer',
    )

    class Meta:
        db_table = 'quiz_option_answer'
        unique_together = ('quiz_answer', 'quiz_option')