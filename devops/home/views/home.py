from django.shortcuts import render, redirect
from django.views.generic import TemplateView


def home(request):
    if request.user.is_authenticated:
        if request.user.is_business:
            return redirect('business:business_home')
        elif request.user.is_student:
            return redirect('student:student_home')
    return redirect('login')


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'
