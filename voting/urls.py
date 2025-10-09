from django.urls import path
from .views import *

app_name = 'voting'

urlpatterns = [
    # Headline urls
    path('headlines/', HeadlineListView.as_view(), name='headline_list'),
    path('headlines/create/', HeadlineCreateView.as_view(), name='headline_create'),
    path('headlines/<uuid:headline_id>/update/', HeadlineCreateView.as_view(), name='headline_update'),
    path('headlines/<uuid:headline_id>/delete/', HeadlineDeleteView.as_view(), name='headline_delete'),
    path('headlines/<uuid:headline_id>/', HeadlineListView.as_view(), name='headline_detail'),
    # Poll urls
    path('polls/', PollListView.as_view(), name='poll_list'),
    path('polls/create/', PollCreateView.as_view(), name='poll_create'),
    path('polls/<uuid:poll_id>/update/', PollCreateView.as_view(), name='poll_update'),
    path('polls/<uuid:poll_id>/delete/', PollDeleteView.as_view(), name='poll_delete'),
    path('polls/<uuid:poll_id>/', PollListView.as_view(), name='poll_detail'),
    # Option urls
    path('options/', OptionListView.as_view(), name='option_list'),
    path('options/create/', OptionCreateView.as_view(), name='option_create'),
    path('options/<uuid:option_id>/update/', OptionCreateView.as_view(), name='option_update'),
    path('options/<uuid:option_id>/delete/', OptionDeleteView.as_view(), name='option_delete'),
    path('options/<uuid:option_id>/',OptionListView.as_view(), name='option_detail'),
    # Vote urls
    path('votes/', VoteListView.as_view(), name='vote_list'),
    path('votes/create/', VoteCreateView.as_view(), name='vote_create'),
    path('votes/<uuid:vote_id>/update/', VoteCreateView.as_view(), name='vote_update'),
    path('votes/<uuid:vote_id>/delete/', VoteDeleteView.as_view(), name='vote_delete'),
    path('votes/<uuid:vote_id>/', VoteListView.as_view(), name='vote_detail'),
]    
