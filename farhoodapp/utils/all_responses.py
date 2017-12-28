from farhoodapp.utils.exception import ValidationError

__author__ = 'DotTech Pvt. Ltd.'

from rest_framework import status
from rest_framework.response import Response


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
            {"status": 'false', "code": resCode, "message": message,
             "data": 'data={"message":"","error": "' + message + '"}'},
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
    def validation_error(result_code,message, data):
        raise ValidationError(
            {"status": False, "code": result_code, "message":message,"data": data},
            status=status.HTTP_200_OK
        )

    def user_object(user):
        user
        return


def raise_validation_error(error_dict):
    raise ValidationError(
        {"status": False, "code": error_dict['result_code'], "values": error_dict['message']},
        status=status.HTTP_200_OK
    )

# def orderObject(order)
