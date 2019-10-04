from django import forms
from student.models import TestTaken
from business.models import Test

class TestIdInputForm(forms.ModelForm):

    # script=forms.FileField()
    '''    testId =forms.CharField(
            label="Test ID",
            widget=forms.NumberInput
        )
    '''

    class Meta:
        model = TestTaken
        fields = [
            'testId'
        ]

    '''
        def clean_testId(self):
            testId = self.cleaned_data.get("testId")
            testId=int(testId)
            if testId not in Test.objects.filter(id=testId):
                self.add_error('testId','Invalid Test Id')
            return testId
    '''
