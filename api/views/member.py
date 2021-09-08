from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (
    CreateMemberSerializer,
    UpdateMemberSerializer,
)
from api.services import update_member, delete_member
from api.utils.exception_handlers import validate_serializer


class UpdateDeleteMemberViewSet(APIView):
    @validate_serializer(serializer=UpdateMemberSerializer)
    def put(self, request, serializer, member_id: int, *args, **kwargs):
        response, status_code = update_member(member_id, serializer.validated_data)
        return Response(response, status=status_code)

    def delete(self, request, member_id: int, *args, **kwargs):
        response, status_code = delete_member(member_id)
        return Response(response, status=status_code)
