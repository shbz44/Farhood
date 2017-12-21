from farhoodapp.models import Event, Comment, Action, EventMember
from farhoodapp.serializers import (UserEventSerializer, EventCommentSerializer, EventActionSerializer,
                                    EventMemberFriendSerializer)


# Get User All Events
def get_user_event(user_id):
    events = Event.objects.filter(user_id=user_id)
    result = UserEventSerializer(events, many=True)
    return result.data


# Get all comments on a certain Event
def get_event_comments(event_id, user_id):
    comments = Comment.objects.filter(event_id=event_id, user_id=user_id)
    result = EventCommentSerializer(comments, many=True)
    return result.data


# Get all actions submitted on a certain even
def get_event_actions(event_id, user_id):
    actions = Action.objects.filter(event_id=event_id, user_id=user_id)
    result = EventActionSerializer(actions, many=True)
    return result.data


# Remove Event Member API
def remove_event_member(event_id, user_id):
    member = EventMember.objects.filter(event_id=event_id, user_id=user_id).first()
    if member:
        member.follow = False
        member.save()
    return 'successfully unfollow'

# Get All Events those are Following
def get_follow_events(follow, user_id):
    follow_events = EventMember.objects.filter(follow=follow, user_id=user_id)
    result = EventMemberFriendSerializer(follow_events, many=True)
    return result.data


# Get All Events those are not Following
def get_unfollow_events(follow, user_id):
    unfollow_events = EventMember.objects.filter(follow=follow, user_id=user_id)
    result = EventMemberFriendSerializer(unfollow_events, many=True)
    return result.data


def get_all_friend_events(event_id, follow=True):
    member = EventMember.objects.filter(event_id=event_id).first()
    result = member.filter(follow)
    return result.data
