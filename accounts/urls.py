from django.urls import path
from accounts import views
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='log_out'),
    path('login/', views.loginuser, name='loginuser')
]