from api.utils.base_enum import BaseEnum


class DocumentType(BaseEnum):
    PUBLIC = 1
    PRIVATE = 2


class MemberStatus(BaseEnum):
    ACTIVE = 1
    INACTIVE = 2


class MemberPermissionType(BaseEnum):
    READ = 1
    READ_WRITE = 2


class FileType(BaseEnum):
    ACTUAL = 1
    VERSION = 2
    REQUEST = 3


class RequestType(BaseEnum):
    REJECTED = 1
    REQUESTED = 2
    APPROVED = 3
