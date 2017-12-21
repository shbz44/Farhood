from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from farhoodapp.models import Event, User, Comment, Action, EventMember


class UserSerializer(serializers.ModelSerializer):
    # SignUp API
    def create(self, validated_data):
        # import pdb;pdb.set_trace()
        user = User.objects._create_user(validated_data.get('email'), validated_data.get('password'))
        if validated_data.get('phone_number'):
            user.phone_number = validated_data.get('phone_number')
        return user

    # Create Profile API
    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get('email', None) or instance.email
    #     instance.password = validated_data.get('password', None) or instance.password
    #     instance.first_name = validated_data.get('first_name', None) or instance.first_name
    #     instance.last_name = validated_data.get('last_name', None) or instance.last_name
    #     instance.phone_number = validated_data.get('phone_number', None) or instance.phone_number
    #     instance.address = validated_data.get('address', None) or instance.address
    #     instance.nick_name = validated_data.get('nick_name', None) or instance.nick_name
    #     instance.image = validated_data.get('image', None) or instance.image
    #     return instance

    class Meta:
        model = User
        exclude = ('username', 'ref_user')


class TemporaryUserSerializer(serializers.ModelSerializer):
    # Import Contacts
    def create(self, validated_data):
        user = User.objects._create_user(validated_data.get('email'), password="123456789")
        return user

    class Meta:
        model = User
        exclude = ('username', 'ref_user')



# Get User All Events
class UserEventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


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

    # user = UserFriendSerializer()

    class Meta:
        model = EventMember
        fields = ('id', 'follow', 'event',)  # 'user', )


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


class EventSerializer(ModelSerializer):
    # Create Event API
    def create(self, validated_data):
        event = Event.objects.create(user=validated_data.get('user'), name=validated_data.get('name'),
                                     description=validated_data.get('description'),
                                     location_name=validated_data.get('location_name'),
                                     location_address=validated_data.get('location_address'))
        return event

    # Edit Event API
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', None) or instance.name
        instance.event_type = validated_data.get('event_type', None) or instance.event_type
        instance.description = validated_data.get('description', None) or instance.description
        instance.scheduled_time = validated_data.get('scheduled_time', None) or instance.scheduled_time
        instance.longitude = validated_data.get('longitude', None) or instance.longitude
        instance.latitude = validated_data.get('latitude', None) or instance.latitude
        instance.location_name = validated_data.get('location_name', None) or instance.location_name
        instance.location_address = validated_data.get('location_address', None) or instance.location_address
        return instance

    class Meta:
        model = Event
        exclude = ('created_at',)
        # fields = ('name', 'event_type', 'description', 'scheduled_time', 'longitude', 'latitude', 'location_name',
        #     'location_address')


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
