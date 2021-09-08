from rest_framework import serializers

from api.models import File


class ListFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'created_at', 'updated_at', 'type')
