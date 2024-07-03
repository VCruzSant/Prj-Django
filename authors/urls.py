from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.regsiter_view, name='register'),
]
