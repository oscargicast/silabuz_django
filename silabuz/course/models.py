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
