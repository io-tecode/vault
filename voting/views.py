from django.shortcuts import render
from .models import *
from django.views.generic import *


# Views for Headline model
class HeadlineListView(ListView, DetailView):
    model = Headline
    template_name = 'voting/headline_list.html'
    context_object_name = 'headlines'
    paginate_by = 10

class HeadlineCreateView(CreateView, UpdateView):
    model = Headline
    template_name = 'voting/headline_form.html'
    fields = ['title', 'subtitle', 'logo', 'header_img']
    success_url = '/headlines/'
    context_object_name = 'headline'
    pk_url_kwarg = 'headline_id'

class HeadlineDeleteView(DeleteView):
    model = Headline
    template_name = 'voting/headline_confirm_delete.html'
    success_url = '/headlines/'
    context_object_name = 'headline'
    pk_url_kwarg = 'headline_id'


# Views for Poll information model
class PollListView(ListView, DetailView):
    model = Poll
    template_name = 'voting/poll_list.html'
    context_object_name = 'polls'
    paginate_by = 10
    pk_url_kwarg = 'poll_id'

class PollCreateView(CreateView, UpdateView):
    model = Poll
    template_name = 'voting/poll_form.html'
    fields = ['headline', 'poll_info']
    success_url = '/polls/'
    context_object_name = 'poll'
    pk_url_kwarg = 'poll_id'

class PollDeleteView(DeleteView):
    model = Poll
    template_name = 'voting/poll_confirm_delete.html'
    success_url = '/polls/'
    context_object_name = 'poll'
    pk_url_kwarg = 'poll_id'


# Views for Option model
class OptionListView(ListView, DetailView):
    model = Option
    template_name = 'voting/option_list.html'
    context_object_name = 'options'
    paginate_by = 10
    pk_url_kwarg = 'option_id'

class OptionCreateView(CreateView, UpdateView):
    model = Option
    template_name = 'voting/option_form.html'
    fields = ['poll', 'option_text']
    success_url = '/options/'
    context_object_name = 'option'
    pk_url_kwarg = 'option_id'

class OptionDeleteView(DeleteView):
    model = Option
    template_name = 'voting/option_confirm_delete.html'
    success_url = '/options/'
    context_object_name = 'option'
    pk_url_kwarg = 'option_id'


# Views for Vote model
class VoteListView(ListView, DetailView):
    model = Vote
    template_name = 'voting/vote_list.html'
    context_object_name = 'votes'
    paginate_by = 10
    pk_url_kwarg = 'vote_id'

class VoteCreateView(CreateView, UpdateView):
    model = Vote
    template_name = 'voting/vote_form.html'
    fields = ['user', 'option', 'poll']
    success_url = '/votes/'
    context_object_name = 'vote'
    pk_url_kwarg = 'vote_id'

class VoteDeleteView(DeleteView):
    model = Vote
    template_name = 'voting/vote_confirm_delete.html'
    success_url = '/votes/'
    context_object_name = 'vote'
    pk_url_kwarg = 'vote_id'


