from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from farhoodapp.models import Event, User, Comment, Action, EventMember


class UserSerializer(serializers.ModelSerializer):
    # SignUp API
    def create(self, validated_data):
        user = User.objects._create_user(validated_data.get('email'), validated_data.get('password'))
        if validated_data.get('phone_number'):
            user.phone_number = validated_data.get('phone_number')
        return user

    class Meta:
        model = User
        exclude = ('username', 'ref_user',)


class TemporaryUserSerializer(serializers.ModelSerializer):
    # Import Contacts
    def create(self, validated_data):
        user = User.objects._create_user(validated_data.get('email'), password="123456789")
        return user

    class Meta:
        model = User
        exclude = ('username', 'ref_user')
#
# class EventContactSerializer(ModelSerializer):
#     user_event = serializers.SerializerMethodField('get_alternate_name')
#
#     def get_alternate_name(self, obj):
#         return obj.user_id
#
#     class Meta:
#         model = Event
#         fields = ('id', 'name', 'user_event',)


class ContactsSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    event_name = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()


    def get_event_name(self, obj):
        events = Event.objects.filter(user_id=obj).first()
        if events:
            return events.name
        else:
            return ""

    def get_name(self, obj):
        name = '{} {}'.format(obj.first_name, obj.last_name)
        return name

    def get_user_id(self, obj):
        return obj.id


    class Meta:
        model = User
        fields = ('name', 'event_name', 'user_id')


class FriendsEventSerializer(serializers.Serializer):
    ref_users = serializers.SerializerMethodField()

    def get_ref_users(self, obj):
        ref_users = ContactsSerializer(obj, many=True)
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
    # user = UserFriendEventSerializer()
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        users = User.objects.filter(id=obj.user.id)
        result = UserFriendEventSerializer(users, many=True)
        return result.data

    class Meta:
        model = EventMember
        fields = ('user',)


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
        fields = ('name', 'account_id', 'image', 'no_of_events', 'participants',)


class CombineNameSerializer(ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        name = '{} {}'.format(obj.first_name, obj.last_name)
        return name

    class Meta:
        model = User
        fields = ('name',)


# Get User All Events
class UserEventSerializer(ModelSerializer):
    user = UserAllSerializer()
    event_member = serializers.SerializerMethodField()

    def get_event_member(self, obj):
        member = EventMember.objects.filter(event_id=obj, follow=False)
        result = EventMemberSerializer(member, many=True)
        return result.data

    class Meta:
        model = Event
        fields = ('id', 'name', 'event_type', 'created_at', 'description', 'scheduled_time', 'longitude', 'latitude',
                  'location_name',
                  'location_address', 'user', 'event_member')


class EventFriendSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'user')


class UserFriendSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# Get All Events those are Following
class EventMemberFriendSerializer(ModelSerializer):
    event = EventFriendSerializer()

    class Meta:
        model = EventMember
        fields = ('id', 'follow', 'event',)


# Get all comments on a certain Event
class EventCommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


# Get all actions submitted on a certain even
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

    # users = serializers.JSONField()

    # Create Event API
    def create(self, validated_data):
        event = Event.objects.create(user=validated_data.get('user'), name=validated_data.get('name'),
                                     description=validated_data.get('description'),
                                     location_name=validated_data.get('location_name'),
                                     location_address=validated_data.get('location_address'), )
        # import pdb;pdb.set_trace()
        # users = validated_data.get('users')
        # event_id = event.id
        # if users:
        #     for member in users:
        #         try:
        #             phone_number = member.get('phone_number')
        #             user_id = User.objects.get(phone_number=phone_number)
        #             request_data = {
        #                 "user": user_id,
        #                 "event": event_id,
        #             }
        #             serializer = FollowEventMemberSerializer(data=request_data)
        #             if serializer.is_valid():
        #                 serializer.save()
        #         except:
        #             pass
        return event

    def get_user_name(self, obj):
        user = User.objects.filter(id=obj.user.id).first()
        # serializer = UserAllSerializer(user, many=False)
        return str(obj.user.first_name) + ' ' + str(obj.user.last_name)

    class Meta:
        model = Event
        fields = ('id', 'name', 'event_type', 'created_at', 'description', 'scheduled_time', 'longitude', 'latitude',
                  'location_name',
                  'location_address', 'user', 'user_name',)


class CommentSerializer(ModelSerializer):
    # Create Comment View
    def create(self, validated_data):
        comment = Comment.objects.create(event=validated_data.get('event'),
                                         user=validated_data.get('user'),
                                         message=validated_data.get('message'))
        return comment

    class Meta:
        model = Comment
        fields = '__all__'


class ActionSerializer(ModelSerializer):
    # Create Action API
    def create(self, validated_data):
        action = Action.objects.create(event=validated_data.get('event'),
                                       user=validated_data.get('user'),
                                       action_type=validated_data.get('action_type'))
        return action

    class Meta:
        model = Action
        fields = '__all__'


class FollowEventMemberSerializer(ModelSerializer):
    # Create Event Member who is Following
    def create(self, validated_data):
        member = EventMember.objects.create(event=validated_data.get('event'),
                                            user=validated_data.get('user'), follow=True)
        return member

    class Meta:
        model = EventMember
        fields = '__all__'


class UnfollowEventMemberSerializer(ModelSerializer):
    # Create Event Member who is not Following
    def create(self, validated_data):
        member = EventMember.objects.create(event=validated_data.get('event'),
                                            user=validated_data.get('user'), follow=False)
        return member

    class Meta:
        model = EventMember
        fields = '__all__'


# Add Event Member API
class AddEventMemberSerializer(ModelSerializer):
    def create(self, validated_data):
        member = EventMember.objects.create(event=validated_data.get('event'),
                                            user=validated_data.get('user'), follow=True)
        return member

    class Meta:
        model = EventMember
        fields = '__all__'
