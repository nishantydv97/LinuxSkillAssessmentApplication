from django.db import transaction
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import CreateView,ListView

from business.models import Test
from student.models import TestTaken
from student.forms import TestIdInputForm
from home.models import Student
from student.scripts.podcrud import PodCrud
from celery import task
from devops import settings
from django.contrib.auth.decorators import login_required

from student.models import TestResult,TestTaken


def student_home(request):
    return render(request, 'student/student_home.html')


class StudentTestIdInputView(CreateView):
    template_name = 'student/student_test_id_input.html'
    form_class = TestIdInputForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.studId = request.user
            instance.result = 0
            instance.save()
            self.request.session['test_taken_id'] = instance.id
            return redirect('student:student_test', id=instance.testId)
        context = {'form': form}
        return render(request, self.template_name, context)


class StudentTestView(View):
    def get(self, request, *args, **kwargs):
        context = {
            # 'q_id': Test.objects.get(id=kwargs['id']).questions.all()[0].id,
            't_id': kwargs['id']
        }

        return render(request, 'student/student_start_test.html', context)


class StudentTestQuestionView(View):
    pod_crud = PodCrud()
    questions = None
    current_que = None
    que_no = None

    # session variables
    # self.request.session['ip_address'][que.id] = {}
    # self.request.session['pod_name'][que.id] = {}
    # self.request.session['que_id'][i] = {}
    # self.request.session['tid']
    # self.request.session['current_que_no']
    # self.request.session['total_que_count']
    # self.request.session['test_taken_id']

    # ---------------------------------------GET-------------------------------------
    def get(self, request, *args, **kwargs):
        self.get_questions()

        self.request.session['current_que_no'] = 0

        # self.request.session['current_que'] = self.questions[self.request.session['current_que_no']]
        current_que = self.questions[self.request.session['current_que_no']]

        # print("heloo---------------------------"+self.request.session['current_que'].title)

        context = {
            "ip": self.request.session['ip_address'][current_que.id],
            "que": current_que.question
        }
        return render(request, 'student/student_test.html', context)

    def get_questions(self):
        self.request.session['tid'] = self.kwargs['tid']

        self.questions = Test.objects.get(id=self.request.session['tid']).questions.all()
        self.request.session['total_que_count'] = self.questions.count()

        # genrate pods for all questions

        # session variables
        self.request.session['ip_address'] = {}
        self.request.session['pod_name'] = {}
        self.request.session['que_id'] = {}
        i = 0
        for que in self.questions:
            name = que.pod_name + "-" + str(self.request.user.id) + "-" + str(self.request.session['tid']) + "-" + str(
                que.id)

            pod_body = self.pod_crud.create_pod_object(pod_name=name)
            ip = self.pod_crud.create_pod(pod_body, name)
            self.request.session['ip_address'][que.id] = ip + ":8765"
            self.request.session['pod_name'][que.id] = name
            self.request.session['que_id'][i] = que.id
            i = i + 1

    # --------------------------------------------POST----------------------------------
    def post(self, request, *args, **kwargs):

        self.questions = Test.objects.get(id=self.request.session['tid']).questions.all()

        self.que_no = str(self.request.session['current_que_no'])
        # Evaluation
        self.evaluate_previous_que()

        # fetch new question if not reached end test
        if self.request.session['current_que_no'] < self.request.session['total_que_count'] - 1:
            self.request.session['current_que_no'] = self.request.session['current_que_no'] + 1
            self.que_no = self.request.session['current_que_no']
            # self.request.session.modified= True

            # self.request.session['current_que'] = self.questions[self.request.session['current_que_no']]
            current_que = self.questions.get(id=self.request.session['que_id'][str(self.que_no)])

            # print("heloo---------------------------"+self.request.session['current_que'].title)

            context = {
                "ip": self.request.session['ip_address'][str(current_que.id)],
                "que": current_que.question
            }
            return render(request, 'student/student_test.html', context)
        elif self.request.session['current_que_no'] == self.request.session['total_que_count'] - 1:
            # result
            testtaken = TestTaken.objects.get(id=self.request.session['test_taken_id'])

            que_attempted = testtaken.test.all()
            score = 0
            for q in que_attempted:
                score += q.result
            testtaken.result = score
            testtaken.save()

            return redirect('student:student_test_result', testtakenid=testtaken.id)

    def evaluate_previous_que(self):

        que = self.questions.get(id=self.request.session['que_id'][self.que_no])
        filename = que.filename()
        path = que.script.path
        pod_name = self.request.session['pod_name'][str(que.id)]
        destinationPath = '/src'
        pod_crud = PodCrud()
        # pod_crud.copy_file_to_pod(filename, path, destinationPath, pod_name)

        # get file
        wget_command = ["wget", settings.current_url + que.script.url]

        pod_crud.execute_on_container(pod_name, wget_command)

        # check result
        exec_command = ["bash", que.filename()]
        result = pod_crud.execute_on_container(pod_name, exec_command)
        # print(result+"   res=========================================")


        # save result
        test_result = TestResult()  # .objects.create()
        test_result.testTakenId_id = self.request.session['test_taken_id']
        test_result.queId = que
        test_result.result = result
        print(test_result)
        test_result.save()


class StudentTakenTestList(ListView):
    template_name = 'student/student_taken_test_list.html'

    def get_queryset(self):
        return TestTaken.objects.filter(studId_id = self.request.user.id)

class StudentTestResultView(View):
    template_name = 'student/student_test_result.html'

    def get(self, request, *args, **kwargs):
        test_taken = TestTaken.objects.get(id=kwargs['testtakenid'])  # (studId= self.request.user.id,testId=test.id) # .order_by('-id')[0]
        # test = Test.objects.get(id=self.kwargs['testtakenid'])
        test=test_taken.testId
        context = {
            'test_id': self.kwargs['testtakenid'],
            'test_name': test,
            'test_result' : test_taken.test.all(),
            'result': test_taken.result
        }
        return render(request, self.template_name, context)
