from django.urls import path, include

from student import views

app_name = 'student'

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', include('home.urls')),
    path('', views.student_home, name='student_home'),
    path('test/', views.StudentTestIdInputView.as_view(), name='student_test_id_input'),
    path('test/<int:id>/', views.StudentTestView.as_view(), name='student_test'),
    path('test/<int:tid>/take/', views.StudentTestQuestionView.as_view(), name='student_test_question'),
    path('test/list/', views.StudentTakenTestList.as_view(),  name='student_taken_test_list'),
    path('test/<int:testtakenid>/result/', views.StudentTestResultView.as_view(),  name='student_test_result'),


]
