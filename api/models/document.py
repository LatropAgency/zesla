from django.contrib.auth.models import User
from django.db import models

from api.models.mixins import DateMixin
from api.utils.enums import DocumentType


class Document(DateMixin):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='own_documents')
    type = models.PositiveSmallIntegerField(choices=DocumentType.items())
    members = models.ManyToManyField(User, through='Member')
