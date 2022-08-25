from django.urls import path

from . import views

urlpatterns = [
    path('customers', views.customer_data, name='customer_data'),
    path('customers/me', views.customer_me_data, name='customer_me_data'),
    path('customers/<str:username>', views.user_data, name='user_data'),
    path('customers/<str:username>/cards', views.cards_customer_data, name='customer_cards'),
    path('loans', views.loans_data, name='loans_data'),
    path('loans/<int:pk>', views.loan_data, name='loan_data'),
    path('branches', views.branches_data, name='branches_data'),
    path('branches/<int:pk>', views.branch_data, name='branch_data'),
    path('cards', views.cards_data, name='cards_data'),
    path('addresses/<int:pk>', views.address_data, name='address_data'),
]
