from django.urls import path, include
from rest_framework import routers

from . import views
from .views import UserViewSet

router = routers.DefaultRouter()
router.register(r'customers', UserViewSet, basename='customer')
router.register(r'addresses', views.AddressViewSet, basename='address')
router.register(r'branches', views.BranchViewSet, basename='branch')

urlpatterns = [
    path('', include(router.urls)),
    path('loans', views.loans_data, name='loans_data'),
    path('loans/<int:pk>', views.loan_data, name='loan_data'),
    path('cards', views.cards_data, name='cards_data'),
]
