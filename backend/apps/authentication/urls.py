from django.urls import path
from . import views


app_name = 'auth'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('verificate/', views.AccountVerification.as_view(), name='verificate')
]
