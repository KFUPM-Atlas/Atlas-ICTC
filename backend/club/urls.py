from django.urls import include, path
from . import views

urlpatterns = [
    path('clubs/<int:club_id>', views.club_details_view, name='get_or_update_club'),
    path('clubs', views.clubs_view, name='create_or_list_clubs')
]