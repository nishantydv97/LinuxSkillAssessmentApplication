import os

from django.db import models
from django.urls import reverse
from home.models import Business
from home.models import User

# Create your models here.


def script_upload_location(instance, filename):
    # filename = instance.title + ".sh"

    return "question/%s/%s" % (instance.title, filename)


class Questions(models.Model):
    title = models.CharField(max_length=50)
    question = models.TextField()
    # marks = models.IntegerField()
    pod_name = models.CharField(max_length=100)
    script = models.FileField(upload_to=script_upload_location, )

    class Meta:
        verbose_name = "question"
        verbose_name_plural = "questions"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('business:question_details', kwargs={"id": self.id})

    def filename(self):
        return os.path.basename(self.script.name)


class Test(models.Model):
    # questions = models.ForeignKey(Questions, on_delete=models.CASCADE)
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    questions = models.ManyToManyField(Questions, related_name='test_questions')
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = "test"
        verbose_name_plural = "tests"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('business:test_details', kwargs={"id": self.id})


class Test_Business(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    def get_test_name(self):
        test = Test.objects.filter(id=self.test.id)
        return test[0].name


'''
from business.models import Test_Business
i=Test_Business.objects.all()
i[0].get_test_name()
'''
