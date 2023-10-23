from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
)

from .serializers import (UserRegistrationSerilizer, ChangePasswordSerializer)
from .models import User

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'message': 'Account successfully created!'},
            status=HTTP_200_OK
        )


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_instance = request.user
        serializer = ChangePasswordSerializer(user_instance, data=request.data)
        if serializer.is_valid():
            if user_instance.check_password(request.data['old_password']):
                if request.data['new_password'] == request.data['confirm_new_password']:
                    user_instance.set_password(request.data['new_password'])
                    user_instance.save()
                    return Response(
                        {'message': 'Password successfully changed!'},
                        status=HTTP_200_OK
                    )
                return Response(
                    {'error': 'Password confirmation field does not math the password!'},
                    status=HTTP_400_BAD_REQUEST
                )
            return Response(
                {'error': 'Incorrect old password!'},
                status=HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    pass


{
    "phone_number": "09305061226",
    "first_name": "Arian",
    "last_name": "Jahed",
    "email": "aj@domain.com",
    "password": "HelloIloveDjango123@",
    "confirm_password": "HelloIloveDjango123@"
}
{
    "old_password": "HelloIloveDjango123@",
    "new_password": "HelloIloveDjang123@",
    "confirm_new_password": "HelloIloveDjang123@"
}
{
    "phone_number": "09111825157",
    "first_name": "Ari",
    "last_name": "Smith",
    "email": "as@domain.com",
    "password": "HelloIloveDjango123@",
    "confirm_password": "HelloIloveDjango123@"
}


