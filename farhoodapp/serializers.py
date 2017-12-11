from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from farhoodapp.models import Action, Comment, Event, EventMember, User

class UserSerializer(serializers.ModelSerializer):

    # def create(self, validated_data):
    #     user_data = validated_data['User']
    #     user, _ = User.objects.get_or_create(email=user_data['email'], password=user_data['password'])
    #     return self

    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8)


    def create(self, validated_data):
        user = User.objects._create_user(validated_data['email'], validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('email', 'password')