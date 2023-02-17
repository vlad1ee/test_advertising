from rest_framework import generics
from rest_framework.response import Response

from user.serializers import UserRegisterSerializer


class UserRegister(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
