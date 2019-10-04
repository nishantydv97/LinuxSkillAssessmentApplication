from django.db import models
from home.models import User
from business.models import Test, Questions


# Create your models here.

class TestTaken(models.Model):
    studId = models.ForeignKey(User, on_delete=models.CASCADE,related_name='stud')
    testId = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test')
    result = models.IntegerField(default=None)


class TestResult(models.Model):
    testTakenId = models.ForeignKey(TestTaken, on_delete=models.CASCADE, related_name='test')
    queId = models.ForeignKey(Questions, on_delete=models.CASCADE, related_name='questions')
    result = models.IntegerField(default=0, blank=None)
