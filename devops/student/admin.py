from django.contrib import admin

from student.models import TestTaken,TestResult

# Register your models here.
admin.site.register(TestResult)
admin.site.register(TestTaken)