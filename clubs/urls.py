from django.urls import path

from . import views

urlpatterns = [
    path('', views.clubs_index, name='clubs'),
]
