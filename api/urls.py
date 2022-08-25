from django.urls import path

from . import views

urlpatterns = [
    path('customers', views.customer_data, name='customer_data'),
    path('customers/me', views.customer_me_data, name='customer_me_data'),
]
