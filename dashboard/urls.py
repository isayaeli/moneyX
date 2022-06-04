from unicodedata import name
from django.urls import path
from .import views
urlpatterns =[
    path('dashboard', views.index, name='dash' ),
    path('deposits', views.deposits, name='deposits'),
    path('withdraw', views.withdraws, name='withdraw'),
    path('address', views.deposit_address, name='address'),
    path('withdraw_address', views.withdraw_address, name='withdraw_address'),
    path('finish', views.finish_withdraw, name='finish'),
    path('track-deposit', views.track_deposit, name='track_deposit'),
    path('binary', views.binary, name='binary'),
    path('verify', views.verify, name='verify'),
    path('binary-agent-withdraw', views.binary_agent_withdraw, name='binary_agent_withdraw'),
    path('swap', views.swap, name='swap'),
    path('trade', views.trade, name='trade'),
]