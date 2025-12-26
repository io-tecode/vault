from django import forms
from .models import *


class HeadlineForm(forms.ModelForm):
    class Meta:
        model = Headline
        exclude = ['creator', 'updated_date']
        widgets = {'allow_vote_changes': forms.CheckboxInput(attrs={'class': 'form-check-input'})}
        

class PollInformationForm(forms.ModelForm):
    class Meta:
        model = Poll_information
        fields = ['Name', 'sub_category']


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['headline', 'poll_info']