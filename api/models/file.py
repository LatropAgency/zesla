from django.db import models

from api.models.mixins import DateMixin
from api.utils.enums import FileType


class File(DateMixin):
    data = models.BinaryField(default=b'')
    hash = models.CharField(max_length=128)
    type = models.PositiveSmallIntegerField(choices=FileType.items(), default=FileType.ACTUAL.value)
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='document_files')
