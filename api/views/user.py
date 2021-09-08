from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.serializers import UserSerializer


class UserAPIView(generics.RetrieveAPIView, generics.CreateAPIView, generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = {
        'get': (IsAuthenticated,),
        'post': (~IsAuthenticated,),
    }

    def get_permissions(self):
        return [permission() for permission in self.permission_classes.get(self.request.method.lower(), [])]

    def get_object(self):
        return self.request.user


class ListUserAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['username']
