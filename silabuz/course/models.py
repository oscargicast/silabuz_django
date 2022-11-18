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

    def __str__(self):
        return f'{self.id}: {self.name}'

    class Meta:
        db_table = 'course'


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


# TODO: Create QuizAnswer and QuizOptionAnswer models.
# With a student relationship.
