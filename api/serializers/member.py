from rest_framework import serializers

from api.models import Member
from api.serializers import UserSerializer


class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Member
        fields = ('id', 'user', 'status', 'permission')


class CreateMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('user', 'status', 'permission')


class UpdateMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('status', 'permission')
