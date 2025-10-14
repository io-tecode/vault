from django.urls import path
from .views import *

app_name = 'voting'

urlpatterns = [
    path('headlines/create/', headline_view, name='headline_create'),
    path('pollinfo/create/', poll_info_view, name='pollinfo_create'),
    path('dashboard/', dashboard_view, name='x6sad_dashboard'),
]    
