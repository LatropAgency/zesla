import functools

from rest_framework import status
from rest_framework.response import Response


def validate_serializer(serializer):
    def wrap(function):
        @functools.wraps(function)
        def wrapper(view, request, *args, **kwargs):
            serializer_to_validate = serializer(data=request.data)
            if serializer_to_validate.is_valid():
                return function(view, request, serializer_to_validate, *args, **kwargs)
            else:
                error_list = {error: serializer_to_validate.errors[error] for error in serializer_to_validate.errors}
                return Response(error_list, status=status.HTTP_400_BAD_REQUEST)

        return wrapper

    return wrap
