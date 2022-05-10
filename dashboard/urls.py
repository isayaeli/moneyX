from unicodedata import name
from django.urls import path
from .import views
urlpatterns =[
    path('dashboard', views.index, name='dash' ),
    path('deposits', views.deposits, name='deposits'),
    path('withdraw', views.withdraws, name='withdraw'),
    path('address', views.deposit_address, name='address'),
    path('withdraw_address', views.withdraw_address, name='withdraw_address'),
    path('finish', views.finish_withdraw, name='finish')
]