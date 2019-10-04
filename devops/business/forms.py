from django import forms
from business.models import Test, Questions


# ---------------------------------------question--------------------------

class QuestionCreateForm(forms.ModelForm):
    title = forms.CharField()
    question = forms.Textarea()

    # script=forms.FileField()

    class Meta:
        model = Questions
        fields = [
            'title',
            'question',
            'pod_name',
            'script'

        ]
    '''
    def clean_title(self):
        title = self.cleaned_data.get("title").upper()
        return title
    '''

# --------------------------------------test-------------------------------
class TestCreateForm(forms.ModelForm):
    questions = forms.ModelMultipleChoiceField(
        queryset=Questions.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = Test
        fields = [
            'name',
            'questions',
        ]
