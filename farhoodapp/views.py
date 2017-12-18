from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from farhoodapp.models import User, Event, Comment, EventMember
from farhoodapp.serializers import (UserSerializer, EventSerializer, CommentSerializer, ActionSerializer,
                                    AddEventMemberSerializer, UnfollowEventMemberSerializer,
                                    FollowEventMemberSerializer)

from farhoodapp.services import get_user_event, get_event_comments, get_event_actions, get_event_member, \
    get_follow_events, get_unfollow_events


# SignUp API
class UserCreate(APIView):
    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"User Created": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Create Profile API
class CreateProfileUser(APIView):
    def post(self, request, format='json'):
        user_id = request.POST.get('user_id')
        if user_id:
            user_data = User.objects.get(id=user_id)
            serializer = UserSerializer(user_data, data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response({"Profile Created": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create Event API
class EventCreateView(APIView):
    def post(self, request, format='json'):
        user_id = request.POST.get('user')
        if user_id:
            serializer = EventSerializer(data=request.data)
            if serializer.is_valid():
                event = serializer.save()
                return Response({"Event Created": EventSerializer(event).data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Edit Event API
class EventEditView(APIView):
    def post(self, request, format='json'):
        user_id = request.POST.get('user')
        if user_id:
            event_data = Event.objects.get(user=user_id)
            serializer = EventSerializer(event_data, data=request.data)
            if serializer.is_valid():
                event = serializer.save()
                return Response({"Event Edited": EventSerializer(event).data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create Comment View
class CreateCommentView(APIView):
    def post(self, request, format='json'):
        user_id = int(request.POST.get('user'))
        event_id = int(request.POST.get('event'))
        if user_id and event_id:
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                comment = serializer.save()
                return Response({"Comment Created": CommentSerializer(comment).data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Create Action API
class CreateActionView(APIView):
    def post(self, request, format='json'):
        user_id = int(request.POST.get('user'))
        event_id = int(request.POST.get('event'))
        if user_id and event_id:
            serializer = ActionSerializer(data=request.data)
            if serializer.is_valid():
                action = serializer.save()
                return Response({"Action Created": ActionSerializer(action).data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Create Event Member who is Following
class CreateFollowEventMemberView(APIView):
    def post(self, request, format='json'):
        user_id = int(request.POST.get('user'))
        event_id = int(request.POST.get('event'))
        # import pdb;pdb.set_trace()
        if user_id and event_id:
            serializer = FollowEventMemberSerializer(data=request.data)
            if serializer.is_valid():
                member = serializer.save()
                return Response({"Event Member Created which is Following": FollowEventMemberSerializer(member).data},
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Create Event Member who is not Following
class CreateUnfollowEventMemberView(APIView):
    def post(self, request, format='json'):
        user_id = int(request.POST.get('user'))
        event_id = int(request.POST.get('event'))
        # import pdb;pdb.set_trace()
        if user_id and event_id:
            check_member = EventMember.objects.filter(event_id=event_id, user_id=user_id).first()
            if not check_member:
                serializer = UnfollowEventMemberSerializer(data=request.data)
                if serializer.is_valid():
                    member = serializer.save()
                    return Response(
                        {"Event Member Created which is not Following": UnfollowEventMemberSerializer(member).data},
                        status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Member Already Exists'}, status=status.HTTP_400_BAD_REQUEST)

#Add Event Member API
class AddEventMemberView(APIView):
    def post(self, request, format='json'):
        user_id = int(request.POST.get('user'))
        event_id = int(request.POST.get('event'))
        # import pdb;pdb.set_trace()
        if user_id and event_id:
            member = EventMember.objects.filter(event_id=event_id, user_id=user_id).first()
            if not member:
                serializer = AddEventMemberSerializer(data=request.data)
                # import pdb;pdb.set_trace()
                if serializer.is_valid():
                    add_member = serializer.save()
                    return Response({"Event Member Added": AddEventMemberSerializer(add_member).data},
                                    status=status.HTTP_201_CREATED)
            else:
                return Response("Member Already Exists")

#Remove Event Member API
class RemoveEventMemberView(APIView):
    def post(self, request, format='json'):
        event_id = int(request.POST.get('event'))
        id = int(request.POST.get('id'))
        # import pdb;pdb.set_trace()
        if event_id and id:
            resp = get_event_member(event_id=event_id, id=id)
            return Response(data=resp, status=status.HTTP_200_OK)

#Get User All Events
class UserEventView(APIView):
    def get(self, request):
        user_id = request.GET.get('user_id', 1)
        resp = {"data": get_user_event(user_id=user_id)}
        return Response(data=resp, status=status.HTTP_200_OK)

#Get all comments on a certain Event
class CommentEventView(APIView):
    def get(self, request):
        event_id = request.GET.get('event_id', 1)
        resp = {"data": get_event_comments(event_id=event_id)}
        return Response(data=resp, status=status.HTTP_200_OK)

#Get all actions submitted on a certain event
class EventActionView(APIView):
    def get(self, request):
        event_id = request.GET.get('event_id', 1)
        resp = {"data": get_event_actions(event_id=event_id)}
        return Response(data=resp, status=status.HTTP_200_OK)

#Get All Events those are Following
class FollowEventView(APIView):
    def get(self, request):
        follow = request.GET.get('follow', True)
        resp = {"data": get_follow_events(follow=follow)}
        return Response(data=resp, status=status.HTTP_200_OK)


#Get All Events those are not Following
class UnfollowEventView(APIView):
    def get(self, request):
        follow = request.GET.get('follow', False)
        resp = {"data": get_unfollow_events(follow=follow)}
        return Response(data=resp, status=status.HTTP_200_OK)
