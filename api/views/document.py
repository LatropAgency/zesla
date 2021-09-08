from typing import Union

from django.db.models import Q
from django.http import HttpResponse, Http404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.models import Document, Member
from api.serializers import (
    RetrieveDocumentSerializer,
    CreateDocumentSerializer,
    UpdateDocumentSerializer,
    ListDocumentSerializer, CreateMemberSerializer,
)
from api.serializers.file import ListFileSerializer
from api.utils.base_converter import PdfConverter, PngConverter
from api.utils.enums import FileType
from api.utils.exception_handlers import validate_serializer
from api.utils.permissions import IsDocumentOwner, IsDocumentMemberForRead


class DocumentViewSet(viewsets.ModelViewSet):
    model = Document
    queryset = Document.objects.filter(is_deleted=False)
    permission_classes = {
        'retrieve': (IsAuthenticated & IsDocumentOwner | IsAuthenticated & IsDocumentMemberForRead,),
        'list': (IsAuthenticated & IsDocumentOwner | IsAuthenticated & IsDocumentMemberForRead,),
        'partial_update': (IsAuthenticated & IsDocumentOwner,),
        'destroy': (IsAuthenticated & IsDocumentOwner,),
        'update': (IsAuthenticated & IsDocumentOwner,),
        'create': (IsAuthenticated,),
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, None)

    def get_permissions(self):
        return [permission() for permission in self.permission_classes.get(self.action, [])]

    def get_queryset(self):
        filters = (Q(owner=self.request.user) | Q(members__in=[self.request.user]),)
        return self.queryset.filter(*filters)

    serializer_classes = {
        'partial_update': UpdateDocumentSerializer,
        'retrieve': RetrieveDocumentSerializer,
        'create': CreateDocumentSerializer,
        'update': UpdateDocumentSerializer,
        'list': ListDocumentSerializer,
    }

    @action(methods=('get',), detail=True)
    def pdf(self, *args, **kwargs) -> Union[Response, HttpResponse]:
        try:
            file = self.get_object().document_files.get(type=FileType.ACTUAL.value)
        except Http404:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        pdf_converter = PdfConverter(file=file)
        pdf_document = pdf_converter.convert()
        return pdf_converter.get_response(pdf_document, 'file.pdf')

    @action(methods=('get',), detail=True)
    def versions(self, *args, **kwargs) -> Union[Response, HttpResponse]:
        try:
            document_versions = self.get_object().document_files.filter(
                type__in=[FileType.ACTUAL.value, FileType.VERSION.value]
            ).order_by('type')
        except Http404:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ListFileSerializer(document_versions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=('get',), detail=True)
    def png(self, *args, **kwargs) -> Union[Response, HttpResponse]:
        try:
            file = self.get_object().document_files.get(type=FileType.ACTUAL.value)
        except Http404:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        png_converter = PngConverter(file=file)
        png_document = png_converter.convert()
        return png_converter.get_response(png_document, 'image.png')

    @validate_serializer(serializer=CreateMemberSerializer)
    @action(methods=('post',), detail=True, url_path='member')
    def create_member(self, request, serializer, *args, **kwargs) -> Response:
        try:
            document = self.get_object()
        except Http404:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        member = Member.objects.create(document=document, **serializer.validated_data)
        serializer = CreateMemberSerializer(member)
        return Response(serializer.data, status=status.HTTP_200_OK)
