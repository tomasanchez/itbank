from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.index, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('reset', views.reset, name='reset_password'),
    path('register', views.register, name='register'),
]
