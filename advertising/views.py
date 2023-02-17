from django.core.exceptions import SuspiciousOperation

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from advertising.models import Advertising
from advertising.serializers import (CreateAdvertisingSerializer,
                                     AdvertisingSerializer,
                                     UpdateStatusAdvertising)

from user.permissions import IsStaffPermission


class AdvertisingAPIView(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data,
                                      context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        if author_id := self.request.query_params.get('author_id'):
            advertisings = Advertising.objects.filter(author=author_id)
        else:
            advertisings = Advertising.objects.all()

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(advertisings, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateAdvertisingSerializer
        return AdvertisingSerializer


class UpdateStatusAdvertisingAPIView(generics.CreateAPIView):
    serializer_class = UpdateStatusAdvertising
    permission_classes = (IsAuthenticated, IsStaffPermission)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        try:
            instances = self.perform_create(serializer)
        except SuspiciousOperation as e:
            return Response(f"{e}", status=403)

        response_serializer = AdvertisingSerializer(instance=instances,
                                                    many=True)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data,
                        status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instances = serializer.save()

        self.check_object_permissions(request=self.request, obj=instances)

        for instance in instances:
            serializer.apply_changes_to_instance(instance)

        return instances
