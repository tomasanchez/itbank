from django.urls import path, include
from rest_framework import routers

from . import views
from .views import UserViewSet

router = routers.DefaultRouter()
router.register(r'customers', UserViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
    path('loans', views.loans_data, name='loans_data'),
    path('loans/<int:pk>', views.loan_data, name='loan_data'),
    path('branches', views.branches_data, name='branches_data'),
    path('branches/<int:pk>', views.branch_data, name='branch_data'),
    path('cards', views.cards_data, name='cards_data'),
    path('addresses/<int:pk>', views.address_data, name='address_data'),
]
