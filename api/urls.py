from django.urls import path, include
from rest_framework import routers

from . import views
from .views import UserViewSet

router = routers.DefaultRouter()

router.register(r'addresses', views.AddressViewSet, basename='address')
router.register(r'branches', views.BranchViewSet, basename='branch')
router.register(r'cards', views.CardViewSet, basename='card')
router.register(r'customers', UserViewSet, basename='customer')
router.register(r'loans', views.LoanViewSet, basename='loan')

urlpatterns = [
    path('', include(router.urls)),
]
