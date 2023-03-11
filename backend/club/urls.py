from django.urls import include, path
from . import views

urlpatterns = [
    # path('clubs', views.create_club, name='create_club'),
    path('clubs/<int:club_id>/', views.club_view, name='get_or_update_club')
]