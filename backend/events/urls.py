from django.urls import include, path
from . import views

urlpatterns = [
    path('events', views.events, name='events'),
    path('events/<int:event_id>/', views.event_details, name='event_details'),
    path('events/<int:event_id>/attend', views.attend_event, name='attend_event')
]