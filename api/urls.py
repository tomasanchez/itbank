from django.urls import path

from . import views

urlpatterns = [
    path('customers', views.customer_data, name='customer_data'),
    path('customers/me', views.customer_me_data, name='customer_me_data'),
    path('loans', views.loans_data, name='loans_data'),
    path('loans/<int:pk>', views.loan_data, name='loan_data'),
]
