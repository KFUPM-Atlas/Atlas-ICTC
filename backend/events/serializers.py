from rest_framework import serializers
from backend.events.models import event
from backend.events.models import event_attendance


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = event
        fields = (
            'event_id',
            'title',
            'registration_link',
            'type',
            'start_datetime',
            'end_datatime',
            'max_attendance',
            'created_at',
            'club_id',
            'poster_path'
        )
