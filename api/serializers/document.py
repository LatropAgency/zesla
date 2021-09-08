from typing import List

from rest_framework import serializers

import hashlib
from api.models import Document, Member, File
from api.serializers import MemberSerializer
from api.utils.enums import FileType


class RetrieveDocumentSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ('id', 'title', 'type', 'file', 'members')

    def get_file(self, obj: Document) -> str:
        """Get file base64 string from bytes"""
        return obj.document_files.get(type=FileType.ACTUAL.value).data.tobytes().decode()

    def get_members(self, obj: Document) -> List[dict]:
        """Get document memebers"""
        return MemberSerializer(Member.objects.filter(document=obj, is_deleted=False), many=True).data


class ListDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'title', 'type', 'created_at', 'updated_at')


class UpdateDocumentSerializer(serializers.ModelSerializer):
    file = serializers.CharField()

    class Meta:
        model = Document
        fields = ('title', 'file', 'type')

    def validate_file(self, value: str) -> bytes:
        """Encode base64 string to bytes"""
        return value.encode()

    def to_representation(self, instance: Document) -> str:
        instance.file = instance.document_files.get(type=FileType.ACTUAL.value).data.tobytes().decode('utf-8')
        return super().to_representation(instance)

    def update(self, instance: Document, validated_data):
        """Update Document instance"""
        file = validated_data.pop('file', instance.document_files.get(type=FileType.ACTUAL.value).data)
        instance.title = validated_data.get('title', instance.title)
        instance.type = validated_data.get('type', instance.title)
        new_hash = hashlib.md5(file).hexdigest()
        if new_hash != instance.document_files.get(type=FileType.ACTUAL.value).hash:
            prev_file = instance.document_files.get(type=FileType.ACTUAL.value)
            prev_file.type = FileType.VERSION.value
            prev_file.save()
            File.objects.create(hash=new_hash, data=file, document=instance)
        return instance


class CreateDocumentSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = ('id', 'title', 'type', 'file')
        read_only_fields = ('id', 'file')

    def get_file(self, obj: Document) -> str:
        """Get document file's base64 string"""
        return obj.document_files.get(type=FileType.ACTUAL.value).data.tobytes().decode('utf-8')

    def create(self, validated_data: dict) -> Document:
        """Create document"""
        new_hash = hashlib.md5(b'').hexdigest()
        document = Document.objects.create(
            owner=self.context['request'].user,
            **validated_data,
        )
        File.objects.create(hash=new_hash, type=FileType.ACTUAL.value, document=document)
        return document
