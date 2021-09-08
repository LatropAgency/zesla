from django.urls import path

from api.views import *
from rest_framework import routers

default_router = routers.DefaultRouter()
default_router.register(r'document', DocumentViewSet)

urlpatterns = [
    path('user/', UserAPIView.as_view()),
    path('users/', ListUserAPIView.as_view()),
    path('document/member/<int:member_id>/', UpdateDeleteMemberViewSet.as_view()),
] + default_router.urls
