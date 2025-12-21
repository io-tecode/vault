from django.urls import path
from .views import *


app_name = 'userauth'

urlpatterns = [
    path('', home, name='home'),
    path('login/', signin, name='login'),
    path('signup/', signup, name='signup'),
    path('verify-email/', email_verification, name='email_verification'),
    path('logout/', signout, name='logout'),
]