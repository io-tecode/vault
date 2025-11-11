from django.urls import path
from .views import *

app_name = 'nominee'

urlpatterns = [
        path('vote/<uuid:headline_id>/', Nominee_view, name='vote'),
        path('vote_success/', vote_success, name='vote_success'),
]