from django.urls import path
from .views import *


app_name = 'voting'

urlpatterns = [
    path('headlines/create/', headline_view, name='headline_create'),
    path('headlines/<uuid:pk>/', headline_detail, name='headline_detail'),
    path('pollinfo/create/', poll_info_view, name='pollinfo_create'),
    path('nominee/<uuid:id>/', nominee_detail, name='nominee_detail'),
    path('dashboard/', dashboard_view, name='x6sad_dashboard'),
    path('shareable_link/<uuid:headline_id>/', generate_shareable_link, name='generate_shareable_link'),
    path('headlines/<uuid:pk>/delete/', headline_delete_simple, name='headline_delete_simple'),
    path('nominee/<uuid:id>/delete/', poll_info_delete, name='poll_info_delete'),
    path('pollinfo/<uuid:id>/edit/', poll_edit, name='poll_edit'),
    path('vote_changes/<uuid:pk>/', vote_changes, name='vote_changes'),
    path('google_auth/<uuid:pk>/', google_auth_requirement, name='google_auth'),
]    
