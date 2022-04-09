from unicodedata import name
from django.urls import path
from .import views
urlpatterns =[
    path('dashboard', views.index, name='dash' ),
    path('deposits', views.deposits, name='deposits')
]