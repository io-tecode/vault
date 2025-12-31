from django.urls import path
from .views import *


app_name = 'nominee'

urlpatterns = [
        path('vote/<uuid:headline_id>/', nominee_view, name='vote'),
        path('vote_success/', vote_success, name='vote_success'),
        path('vote_log/<uuid:headline_id>/', nominee_logs, name='analyze_votes'),
        path('google-auth/<uuid:headline_id>/', google_oauth_vote, name='google_oauth_vote'),
]