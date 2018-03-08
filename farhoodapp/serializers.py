import re
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator

from farhoodapp.models import Event, User, Comment, Action, EventMember


class EmailValidator(object):
    def __init__(self, message):
        self.message = message

    def __call__(self, email):
        email_re = "^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$"
        if not re.match(email_re, email):
            raise serializers.ValidationError(self.message, code='invalid-email')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=3)
    email = serializers.EmailField(
        validators=[EmailValidator(message="Invaid email address"), UniqueValidator(queryset=User.objects.all())],
        required=True)
    phone_regex = RegexValidator(regex=r'^\+?[0,9]?\d{10,15}$',
                                 message="Phone number must be entered in the format: '+999999999999'. Minimum 10 and Maximum 15 digits allowed.")
    phone_number = serializers.CharField(validators=[phone_regex, UniqueValidator(queryset=User.objects.all())],
                                         max_length=15, allow_null=True, allow_blank=True,
                                         required=False)

    def create(self, validated_data):
        user = User.objects._create_user(validated_data.get('email'), validated_data.get('password'))
        if validated_data.get('phone_number'):
            user.phone_number = validated_data.get('phone_number')
            user.save()
        return user

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'password',)


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone_number',)


class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=3)
    email = serializers.EmailField(
        validators=[EmailValidator(message="Invaid email address"), UniqueValidator(queryset=User.objects.all())],
        required=True)
    phone_regex = RegexValidator(regex=r'^\+?[0,9]?\d{10,15}$',
                                 message="Phone number must be entered in the format: '+999999999999'. Minimum 10 and Maximum 15 digits allowed.")
    phone_number = serializers.CharField(validators=[phone_regex, UniqueValidator(queryset=User.objects.all())],
                                         max_length=15, allow_null=True, allow_blank=True,
                                         required=False)

    name_regex = RegexValidator(regex=r'^[a-zA-Z]+(([a-zA-Z ])?[a-zA-Z]*)*$',
                                message='No special characters and digits allowed.')
    first_name = serializers.CharField(validators=[name_regex], max_length=150, allow_null=True, allow_blank=True,
                                       required=False)
    last_name = serializers.CharField(validators=[name_regex], max_length=150, allow_null=True, allow_blank=True,
                                      required=False)
    nick_name = serializers.CharField(validators=[name_regex], max_length=150, allow_null=True, allow_blank=True,
                                      required=False)

    address_regex = RegexValidator(regex=r'^[a-zA-Z0-9\s,\-]+$',
                                   message='No special characters except space, comma and dashes')
    address = serializers.CharField(validators=[address_regex], max_length=150, allow_null=True, allow_blank=True,
                                    required=False)

    username_regex = RegexValidator(regex=r'^[a-zA-Z0-9\s\-]+$',
                                    message='No special characters except space, and dashes')
    username = serializers.CharField(validators=[username_regex], max_length=50, required=False)

    def create(self, validated_data):
        user = User.objects._create_user(validated_data.get('email'), validated_data.get('password'))
        if validated_data.get('phone_number'):
            user.phone_number = validated_data.get('phone_number')
            user.save()
        return user

    class Meta:
        model = User
        fields = (
            'email', 'phone_number', 'password', 'first_name', 'last_name', 'nick_name', 'username', 'address',
            'image',)


class ProfileUpdateSerializer(ModelSerializer):
    phone_regex = RegexValidator(regex=r'^\+?[0,9]?\d{10,15}$',
                                 message="Phone number must be entered in the format: '+999999999999'. Minimum 10 and Maximum 15 digits allowed.")
    phone_number = serializers.CharField(validators=[phone_regex, UniqueValidator(queryset=User.objects.all())],
                                         max_length=15, allow_null=True, allow_blank=True,
                                         required=False)

    name_regex = RegexValidator(regex=r'^[a-zA-Z]+(([a-zA-Z ])?[a-zA-Z]*)*$',
                                message='No special characters and digits allowed.')
    first_name = serializers.CharField(validators=[name_regex], max_length=150, allow_null=True, allow_blank=True,
                                       required=False)
    last_name = serializers.CharField(validators=[name_regex], max_length=150, allow_null=True, allow_blank=True,
                                      required=False)
    nick_name = serializers.CharField(validators=[name_regex], max_length=150, allow_null=True, allow_blank=True,
                                      required=False)

    address_regex = RegexValidator(regex=r'^[a-zA-Z0-9\s,\-]+$',
                                   message='No special characters except space, comma and dashes')
    address = serializers.CharField(validators=[address_regex], max_length=150, allow_null=True, allow_blank=True,
                                    required=False)

    username_regex = RegexValidator(regex=r'^[a-zA-Z0-9\s\-]+$',
                                    message='No special characters except space, and dashes')
    username = serializers.CharField(validators=[username_regex], max_length=50, required=False)

    class Meta:
        model = User
        fields = ('phone_number', 'first_name', 'last_name', 'nick_name', 'username', 'address', 'image',)


class TemporaryUserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects._create_user(validated_data.get('email'), password="123456789")
        return user

    class Meta:
        model = User
        fields = ('email', 'password',)


class FriendsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    event = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()

    def get_event(self, obj):
        event = Event.objects.filter(user_id=obj).order_by('-id').first()
        if event:
            return EventSerializer(event).data
        else:
            return {}

    def get_name(self, obj):
        return obj.first_name

    def get_user_id(self, obj):
        return obj.id

    class Meta:
        model = User
        fields = ('name', 'event', 'user_id', 'phone_number')


class FriendsEventSerializer(serializers.Serializer):
    ref_users = serializers.SerializerMethodField()

    def get_ref_users(self, obj):
        ref_users = FriendsSerializer(obj, many=True)
        return ref_users.data

    class Meta:
        fields = ('ref_users',)


class UserAllSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        name = '{} {}'.format(obj.first_name, obj.last_name)
        return name

    class Meta:
        model = User
        fields = ('name',)


class UserFriendEventSerializer(ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        name = '{} {}'.format(obj.first_name, obj.last_name)
        return name

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phone_number')


class UserImageSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('image',)


class EventMemberSerializer(ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        users = User.objects.filter(id=obj.user.id).first()
        result = UserFriendEventSerializer(users, many=False)
        return result.data

    class Meta:
        model = EventMember
        fields = ('user',)


class UserEventMemberSerializer(ModelSerializer):
    user_id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()

    def get_user_id(self, obj):
        userr = User.objects.filter(id=obj.user.id).first()
        return userr.id

    def get_name(self, obj):
        userr = User.objects.filter(id=obj.user.id).first()
        return str(userr.first_name) + " " + str(userr.last_name)

    def get_phone_number(self, obj):
        userr = User.objects.filter(id=obj.user.id).first()
        return userr.phone_number

    class Meta:
        model = EventMember
        fields = ('user_id', 'name', 'phone_number')


class EventOrganisedSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ('id',)


class UserProfileSerializer(ModelSerializer):
    name = serializers.SerializerMethodField()
    no_of_events = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()

    def get_name(self, obj):
        name = '{} {}'.format(obj.first_name, obj.last_name)
        return name

    def get_no_of_events(self, obj):
        events = Event.objects.filter(user_id=obj).count()
        return events

    def get_participants(self, obj):
        events = Event.objects.filter(user_id=obj)
        participant = EventMember.objects.filter(event__in=events).count()
        return participant

    class Meta:
        model = User
        fields = ('id', 'name', 'image', 'no_of_events', 'participants',)


class CombineNameSerializer(ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        name = '{} {}'.format(obj.first_name, obj.last_name)
        return name

    class Meta:
        model = User
        fields = ('name',)


class CommentUserSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class UserEventSerializer(ModelSerializer):
    user = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    event_member = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_event_member(self, obj):
        member = EventMember.objects.filter(event_id=obj, follow=True)
        result = UserEventMemberSerializer(member, many=True)
        return result.data

    def get_user(self, obj):
        name = '{} {}'.format(obj.user.first_name, obj.user.last_name)
        return name

    def get_user_id(self, obj):
        return obj.user.id

    def get_comments(self, obj):
        comments = Comment.objects.filter(event=obj).order_by('-created_at')
        return CommentUserSerializer(comments, many=True).data

    class Meta:
        model = Event
        fields = ('id', 'name', 'event_type', 'created_at', 'description', 'scheduled_time', 'longitude', 'latitude',
                  'location_name', 'location_address', 'user', 'event_member', 'comments', 'user_id')


class EventFriendSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'user')


class UserFriendSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class EventMemberFriendSerializer(ModelSerializer):
    event = EventFriendSerializer()

    class Meta:
        model = EventMember
        fields = ('id', 'follow', 'event',)


class EventCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class EventActionSerializer(ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'


class EventMemberRemoveSerializer(ModelSerializer):
    class Meta:
        model = EventMember
        fields = '__all__'


class EventUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)


class EventSerializer(ModelSerializer):
    user_name = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

    def get_members(self, event):
        members = EventMember.objects.filter(event=event)
        return FollowEventMemberSerializer(members, many=True).data

    def create(self, validated_data):
        event = Event.objects.create(user=validated_data.get('user'), name=validated_data.get('name'),
                                     description=validated_data.get('description'),
                                     location_name=validated_data.get('location_name'),
                                     location_address=validated_data.get('location_address'),
                                     longitude=validated_data.get('longitude', 0.0),
                                     latitude=validated_data.get('latitude', 0.0),
                                     event_type=validated_data.get('event_type', 'coffee'),
                                     scheduled_time=validated_data.get('scheduled_time'))

        return event

    def get_user_name(self, obj):
        user = User.objects.filter(id=obj.user.id).first()
        return str(user.first_name) + ' ' + str(user.last_name)

    class Meta:
        model = Event
        fields = ('id', 'name', 'event_type', 'created_at', 'description', 'scheduled_time', 'longitude', 'latitude',
                  'location_name', 'location_address', 'user', 'user_name', 'members')


class CommentSerializer(ModelSerializer):
    def create(self, validated_data):
        comment = Comment.objects.create(event=validated_data.get('event'),
                                         user=validated_data.get('user'),
                                         message=validated_data.get('message'))
        return comment

    class Meta:
        model = Comment
        fields = '__all__'


class ActionSerializer(ModelSerializer):
    def create(self, validated_data):
        action = Action.objects.create(event=validated_data.get('event'),
                                       user=validated_data.get('user'),
                                       action_type=validated_data.get('action_type', 'good'))
        return action

    class Meta:
        model = Action
        fields = '__all__'


class FollowEventMemberSerializer(ModelSerializer):
    def create(self, validated_data):
        member = EventMember.objects.create(event=validated_data.get('event'),
                                            user=validated_data.get('user'), follow=True)
        return member

    class Meta:
        model = EventMember
        fields = '__all__'


class UnfollowEventMemberSerializer(ModelSerializer):
    def create(self, validated_data):
        member = EventMember.objects.create(event=validated_data.get('event'),
                                            user=validated_data.get('user'), follow=False)
        return member

    class Meta:
        model = EventMember
        fields = '__all__'


class AddEventMemberSerializer(ModelSerializer):
    def create(self, validated_data):
        member = EventMember.objects.create(event=validated_data.get('event'),
                                            user=validated_data.get('user'), follow=validated_data.get('follow'))
        return member

    class Meta:
        model = EventMember
        fields = '__all__'
