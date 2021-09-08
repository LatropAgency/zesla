from rest_framework import status

from api.models import Member
from api.serializers import MemberSerializer


def update_member(member_id: int, member_data: dict):
    Member.objects.filter(pk=member_id, is_deleted=False).update(**member_data)
    try:
        members = Member.objects.get(pk=member_id)
    except Member.DoesNotExist:
        return {'member': 'DOES_NOT_EXISTS'}, status.HTTP_404_NOT_FOUND
    serializer = MemberSerializer(members, many=True)
    return serializer.data, status.HTTP_200_OK


def delete_member(member_id: int):
    try:
        member = Member.objects.get(pk=member_id, is_deleted=False)
    except Member.DoesNotExist:
        return {'member': 'DOES_NOT_EXISTS'}, status.HTTP_404_NOT_FOUND
    member.delete()
    serializer = MemberSerializer(member)
    return serializer.data, status.HTTP_200_OK
