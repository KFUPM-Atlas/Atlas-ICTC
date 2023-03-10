from abc import ABC

from rest_framework import serializers
from .models import event


class EventSerializer(serializers.ModelSerializer):
    event_id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(allow_null=False, required=True)
    description = serializers.CharField(allow_null=False, required=True)
    registration_link = serializers.URLField(allow_null=True, required=False, default=None)
    type = serializers.CharField(allow_null=True, required=False)
    start_datetime = serializers.DateTimeField(allow_null=False, required=True)
    end_datetime = serializers.DateTimeField(allow_null=False, required=True)
    max_attendance = serializers.IntegerField(allow_null=True, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    club_id = serializers.IntegerField(allow_null=False, required=True)
    poster_path = serializers.URLField(allow_null=True, required=False, default=None)

    def validate(self, data):
        validated_data = super().validate(data)
        if data['end_datetime'] <= data['start_datetime']:
            raise serializers.ValidationError('end_datetime must be after start_datetime')
        return validated_data

    class Meta:
        model = event
        fields = (
            'event_id',
            'title',
            'description',
            'registration_link',
            'type',
            'start_datetime',
            'end_datetime',
            'max_attendance',
            'created_at',
            'club_id',
            'poster_path'
        )


