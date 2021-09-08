from django.contrib.auth.models import User
from django.db import models

from api.models.mixins import DateMixin
from api.utils.enums import MemberStatus, MemberPermissionType


class Member(DateMixin):
    document = models.ForeignKey('Document', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=MemberStatus.items())
    permission = models.PositiveSmallIntegerField(choices=MemberPermissionType.items())

    class Meta:
        unique_together = [['document', 'user']]
