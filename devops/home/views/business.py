from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import CreateView

from home.models import User
from home.forms import BusinessSignUpForm

class BusinessSignUpView(CreateView):
    model = User
    form_class = BusinessSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'business'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('business:business_home')
