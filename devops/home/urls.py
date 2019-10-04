from django.urls import include, path
from home.views import home, student, business

urlpatterns = [
    path('', home.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', home.SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', student.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/business/', business.BusinessSignUpView.as_view(), name='business_signup'),

]