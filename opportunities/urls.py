from django.urls import path

from . import views

urlpatterns = [
    path('', views.opportunities_index, name='opportunities'),
    path('post/', views.create_post, name='create_opportunity_post'),
]
