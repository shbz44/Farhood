from farhoodapp.models import Event, Comment, Action, EventMember, User
from farhoodapp.serializers import (UserEventSerializer, EventCommentSerializer, EventActionSerializer,
                                    EventMemberFriendSerializer, UserProfileSerializer,
                                    UserImageSerializer, FriendsEventSerializer)


def get_user_event(user_id):
    events = Event.objects.filter(user_id=user_id).order_by('-created_at').first()
    result = UserEventSerializer(events, many=False)
    return result.data


def get_user_image_url(id, request=None):
    user_image = User.objects.get(id=id)
    result = UserImageSerializer(user_image, context={'request': request}, many=False)
    return result.data


def get_user_profile(id, request=None):
    users = User.objects.filter(id=id).first()
    result = UserProfileSerializer(users, context={'request': request}, many=False)
    return result.data


def get_event_comments(event_id, user_id):
    comments = Comment.objects.filter(event_id=event_id, user_id=user_id)
    result = EventCommentSerializer(comments, many=True)
    return result.data


def get_event_actions(event_id, user_id):
    actions = Action.objects.filter(event_id=event_id, user_id=user_id)
    result = EventActionSerializer(actions, many=True)
    return result.data


def remove_event_member(event_id, user_id):
    member = EventMember.objects.filter(event_id=event_id, user_id=user_id).first()
    if member:
        member.follow = False
        member.save()
    return 'successfully unfollowed'


def get_follow_events(follow, user_id):
    follow_events = EventMember.objects.filter(follow=follow, user_id=user_id)
    result = EventMemberFriendSerializer(follow_events, many=True)
    return result.data


def get_unfollow_events(follow, user_id):
    unfollow_events = EventMember.objects.filter(follow=follow, user_id=user_id)
    result = EventMemberFriendSerializer(unfollow_events, many=True)
    return result.data


def get_friends_list(id):
    friends = User.objects.filter(id=id).first()
    ref_users = friends.ref_user.filter(temporary_profile=False)
    result = FriendsEventSerializer(ref_users, many=False)
    return result.data


def get_contacts_list(id):
    contacts = User.objects.filter(id=id).first()
    ref_users = contacts.ref_user.all()
    result = FriendsEventSerializer(ref_users, many=False)
    return result.data
