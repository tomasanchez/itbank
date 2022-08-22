from django.urls import path

from cuentas import views as account_views
from tarjetas import views as card_views
from . import views

urlpatterns = [
    path('me', views.index, name='me'),
    path('me/splitter', views.split_expenses, name='split_expenses'),
    path('me/accounts', account_views.index, name='my-accounts'),
    path('me/cards', card_views.my_cards, name='my-cards'),
]
