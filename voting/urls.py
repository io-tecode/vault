from django.urls import path
from .views import *

app_name = 'voting'

urlpatterns = [
    path('headlines/create/', headline_view, name='headline_create'),
    path('headlines/<uuid:pk>/', headline_detail, name='headline_detail'),
    path('pollinfo/create/', poll_info_view, name='pollinfo_create'),
    path('votee/<uuid:id>/', votee_detail, name='votee_detail'),
    path('dashboard/', dashboard_view, name='x6sad_dashboard'),
    # path('polls/<int:pk>/edit/', poll_edit_view, name='poll_edit'),
    # path('polls/<int:pk>/delete/', poll_delete_view, name='poll_delete'),
    
    path('shareable_link/<uuid:headline_id>/', generate_shareable_link, name='generate_shareable_link'),
]    
