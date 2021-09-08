from rest_framework.permissions import BasePermission, SAFE_METHODS

from api.models import Document


class IsDocumentOwner(BasePermission):
    def has_object_permission(self, request, view, obj: Document) -> bool:
        return obj.owner == request.user


class IsDocumentMemberForRead(BasePermission):
    def has_object_permission(self, request, view, obj: Document) -> bool:
        return request.user in obj.members.all() and request.method in SAFE_METHODS
