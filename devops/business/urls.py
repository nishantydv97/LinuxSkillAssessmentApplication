from django.urls import path, include, re_path
from business import views


app_name = 'business'

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', include('home.urls')),
    path('', views.business_home, name='business_home'),

    path('question/', views.QuestionListView.as_view(),name='question_create'),
    path('question/create/', views.QuestionCreateView.as_view(),name='question_create'),
    path('question/<int:id>/', views.QuestionDetailView.as_view(), name='question_details'),
    # path('question/<int:id>/update/', views.QuestionUpdateView.as_view(), name='question_update'),



    path('test/create/', views.TestCreateView.as_view(), name='test_create'),
    path('test/<int:id>/', views.TestDetailView.as_view(), name='test_details'),
    path('test/<int:id>/update', views.TestUpdateView.as_view(), name='test_update'),
    path('test/', views.TestListView.as_view(), name='test_list'),
    path('test/<int:id>/result/', views.TestResultView.as_view(), name='test_result'),


]
