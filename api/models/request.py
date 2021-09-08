from django.contrib.auth.models import User
from django.db import models

from api.models.mixins import DateMixin
from api.utils.enums import RequestType


class Request(DateMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    comment = models.CharField(max_length=255)
    file = models.ForeignKey('File', on_delete=models.CASCADE, related_name='request')
    type = models.PositiveSmallIntegerField(choices=RequestType.items(), default=RequestType.REQUESTED.value)
