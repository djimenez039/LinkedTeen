from django.urls import path

from . import views

urlpatterns = [
    path('', views.clubs_index, name='clubs'),
    path('<int:club_id>/', views.club_detail, name='club_detail'),
    path('<int:club_id>/join/', views.join_club, name='join_club'),
    path('<int:club_id>/posts/', views.create_club_post, name='create_club_post'),
    path('<int:club_id>/edit/', views.edit_club, name='edit_club'),
]
