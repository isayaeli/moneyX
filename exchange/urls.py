from django.urls import path
from .import views
urlpatterns = [
  path('processing-exchanging', views.exchanging, name="exchanging")
]