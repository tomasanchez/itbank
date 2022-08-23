from django.urls import path

from cuentas import views as account_views
from tarjetas import views as card_views
from . import views

urlpatterns = [
    path('me', views.index, name='me'),
    path('me/splitter', views.split_expenses, name='split_expenses'),
    path('me/accounts', account_views.index, name='my-accounts'),
    path('me/accounts/<int:pk>', account_views.details_page, name='my-accounts-details'),
    path('me/transfer', account_views.transfer_page, name='transfers'),
    path('me/cards', card_views.my_cards, name='my-cards'),
]
