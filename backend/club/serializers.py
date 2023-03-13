from rest_framework import serializers
from .models import club

class ClubSerializer(serializers.ModelSerializer):
    club_id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(allow_null=False, required=True)
    type = serializers.CharField(allow_null=True, required=False)
    description = serializers.CharField(allow_null=False, required=True)
    headquarter = serializers.CharField(allow_null=False, required=True)
    supervisor_id = serializers.IntegerField(allow_null=False, required=True)
    logo_path = serializers.URLField(allow_null=True, required=False, default=None)

    class Meta:
        model = club
        fields = (
            'club_id',
            'name',
            'type',
            'description',
            'headquarter',
            'supervisor_id',
            'logo_path'
        )

