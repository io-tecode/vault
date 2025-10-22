from django import forms
from .models import *


class HeadlineForm(forms.ModelForm):
    class Meta:
        model = Headline
        # fields = ['title', 'subtitle', 'logo', 'header_img']
        exclude = ['creator', 'updated_date']
        


class PollInformationForm(forms.ModelForm):
    class Meta:
        model = Poll_information
        fields = ['Name', 'sub_category']


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['headline', 'poll_info']


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['poll', 'opttext']


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['user', 'option', 'poll']

