from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from farhoodapp.serializers import UserSerializer
from django.contrib.auth.models import User


class UserCreate(APIView):
    """
    Creates the user.
    """

    # def post(self, request, format='json'):
    #     return Response('hello')


    # def post(self, request):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(True, status.HTTP_200_OK, "Success", {})
    #     return Response(False, status.HTTP_400_BAD_REQUEST, "Success", {})

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response({"User Created."}, status=status.HTTP_201_CREATED)