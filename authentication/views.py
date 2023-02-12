from django.contrib.auth.models import User

from authentication.permissions import UserPermission
from authentication.serializers import RegisterSerializer
from rest_framework import viewsets, mixins


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [UserPermission]
    serializer_class = RegisterSerializer
