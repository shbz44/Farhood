from django.db.models import Q

from farhoodapp.exception import ValidationError
from farhoodapp.models import User
from farhoodapp.serializers import FollowEventMemberSerializer

__author__ = 'DotTech Pvt. Ltd.'

from rest_framework import status
from rest_framework.response import Response
import json


class CustomResponse():
    def __init__(self):
        pass

    @staticmethod
    def create_response(stat, resCode, message, data):
        return Response(
            {"status": stat, "code": resCode, "message": message, "data": data},
            status=status.HTTP_200_OK
        )

    @staticmethod
    def create_error_response(resCode, message):
        return Response(
            {"status": 'false', "code": resCode, "message": message},
            status=status.HTTP_200_OK
        )

    @staticmethod
    def create_response_with_key(response_code, data, pop_key_into):
        data[pop_key_into] = data.pop('results')
        return CustomResponse.create_response(response_code, data)

    # @staticmethod
    # def raise_validation_error(error_dict):
    #     raise ValidationError(
    #         {"status": False, "code": error_dict['result_code'], "values": error_dict['message']},
    #         status=status.HTTP_200_OK
    #     )

    @staticmethod
    def validation_error(result_code, message, data):
        raise ValidationError(
            {"status": False, "code": result_code, "message": message, "data": data},
            status=status.HTTP_200_OK
        )

    def user_object(user):
        return user


def raise_validation_error(error_dict):
    raise ValidationError(
        {"status": False, "code": error_dict['result_code'], "values": error_dict['message']},
        status=status.HTTP_200_OK
    )


def search_user(data):
    phone_number = data.get('phone_number') or '0981726394'
    user = User.objects.filter(Q(email=data.get('email')) | Q(phone_number=phone_number)).first()
    if user:
        user.set_password(data.get('password'))
        user.temporary_profile = False
        user.save()
    return user


def connect_members_with_event(event, users):
    if users:
#        users = json.loads(users)
        for member in users:
            try:
                phone_number = member.get('phone_number')
                user = User.objects.filter(phone_number=phone_number).first()
                request_data = {
                    "user": user.id,
                    "event": event.id,
                }
                serializer = FollowEventMemberSerializer(data=request_data)
                if serializer.is_valid():
                    serializer.save()
            except:
                pass
