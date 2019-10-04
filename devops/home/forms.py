from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.db import transaction
from django import forms

from home.models import User, Student, Business


class StudentSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True, label='First Name')
    last_name = forms.CharField(required=True, label='Last Name')
    email = forms.EmailField(required=True, label='Email')
    contact_no = forms.CharField(
        required=True,
        validators=[RegexValidator('^[0-9]{10}$', message="Enter valid contact number")],
        label='Contact Number')

    class Meta(UserCreationForm.Meta):
        model = User
        # fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        # fields_required = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    @transaction.atomic
    def save(self, commit=True):

        user = super().save(commit=False)
        user.is_student = True
        user.email = (self.cleaned_data.get('email'))
        user.save()
        student = Student.objects.create(user=user)
        # student.first_name.add(*self.cleaned_data.get('first_name'))
        student.first_name = (self.cleaned_data.get('first_name'))
        student.last_name = (self.cleaned_data.get('last_name'))
        student.contact_no = (self.cleaned_data.get('contact_no'))

        student.save()
        return user


class BusinessSignUpForm(UserCreationForm):
    organization_name = forms.CharField(required=True, label='Organization Name')
    email = forms.EmailField(required=True, label='Email')

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self, commit=True):

        user = super().save(commit=False)
        user.is_business = True
        user.email = (self.cleaned_data.get('email'))
        user.save()
        business = Business.objects.create(user=user)
        # student.first_name.add(*self.cleaned_data.get('first_name'))
        business.organization_name = (self.cleaned_data.get('organization_name'))

        business.save()
        return user
