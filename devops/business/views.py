from django.shortcuts import render, get_object_or_404
from django.views import View

# Create your views here.
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from business.models import Test, Questions, Test_Business
from business.forms import TestCreateForm, QuestionCreateForm
from student.models import TestTaken


def business_home(request):
    return render(request, 'business/business_home.html')


# ------------------------------------------questions----------------------------------

class QuestionCreateView(CreateView):
    template_name = 'business/question/question_create.html'
    form_class = QuestionCreateForm
    queryset = Questions.objects.all()


'''
    def form_valid(self, form):
        print("hello"+form.cleaned_data)
        return super().form_valid(form)


'''
class QuestionListView(ListView):
    template_name = 'business/question/question_list.html'
    queryset = Questions.objects.all()

class QuestionDetailView(DetailView):
    template_name = 'business/question/question_detail.html'

    def get_object(self, queryset=None):
        id_ = self.kwargs.get('id')

        return get_object_or_404(Questions, id=id_)


class QuestionUpdateView(UpdateView):
    template_name = 'business/question/question_update.html'


# -------------------------------------------test--------------------------------------
class TestListView(ListView):
    template_name = 'business/test/test_list.html'

    def get_queryset(self):
        return Test_Business.objects.filter(business_id=self.request.user.id)


class TestCreateView(CreateView):
    template_name = 'business/test/test_create.html'
    form_class = TestCreateForm
    queryset = Test.objects.all()

    def form_valid(self, form):
        test = form.save()
        test_business = Test_Business.objects.create(business_id=self.request.user.id, test_id=test.id)
        test_business.save()
        return super().form_valid(form)


class TestDetailView(DetailView):
    template_name = 'business/test/test_detail.html'

    # queryset = Test.objects.all()

    def get_object(self, queryset=None):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Test, id=id_)


class TestUpdateView(UpdateView):
    template_name = 'business/test/test_update.html'


class TestResultView(ListView):
    template_name = 'business/test/test_result.html'
    # queryset = Test_Business.objects.filter(business=self.request.user)
    '''
        def get(self,request,*args,**kwargs):

        context={

        }
        return render(request,self.template_name,context)
    
    def get_queryset(self):
        return Test_Business.objects.filter(business_id=self.request.user.id)
    '''
    def get_queryset(self):
        id_ = self.kwargs.get('id')
        return TestTaken.objects.filter(testId_id =id_).order_by('-result')
