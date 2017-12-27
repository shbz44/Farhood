from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from farhoodapp.models import User, Event, Comment, EventMember
from farhoodapp.serializers import (UserSerializer, EventSerializer, CommentSerializer, ActionSerializer,
                                    AddEventMemberSerializer, UnfollowEventMemberSerializer,
                                    FollowEventMemberSerializer, TemporaryUserSerializer)

from farhoodapp.services import (get_user_event, get_event_comments, get_event_actions, get_follow_events,
                                 get_unfollow_events, remove_event_member, )


# SignUp API
class UserCreate(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)

    def post(self, request, format='json'):
        data = request.data.copy()
        if 'email' not in data.keys():
            data['email'] = data['phone_number'] + "@dottech.info"
        else:
            data['email'] = data['email']
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"User Created": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create Profile API
class CreateProfileUser(APIView):
    def put(self, request, format='json'):
        user_data = request.user
        serializer = UserSerializer(user_data, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"Profile Created": UserSerializer(user).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create Event API
class EventCreateView(APIView):
    def post(self, request, format='json'):
        parser_classes = (MultiPartParser,)
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        serializer = EventSerializer(data=request_data)
        if serializer.is_valid():
            event = serializer.save()
            return Response({"Event Created": EventSerializer(event).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Edit Event API
class EventEditView(APIView):
    def post(self, request, format='json'):
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        id = request.POST.get('id')
        event_data = Event.objects.get(id=id, user=request.user)
        serializer = EventSerializer(event_data, data=request_data)
        if serializer.is_valid():
            event = serializer.save()
            return Response({"Event Edited": EventSerializer(event).data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create Comment View
class CreateCommentView(APIView):
    def post(self, request, format='json'):
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        event_id = int(request.POST.get('event'))
        if event_id:
            serializer = CommentSerializer(data=request_data)
            if serializer.is_valid():
                comment = serializer.save()
                return Response({"Comment Created": CommentSerializer(comment).data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create Action API
class CreateActionView(APIView):
    def post(self, request, format='json'):
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        event_id = int(request.POST.get('event'))
        if event_id:
            serializer = ActionSerializer(data=request_data)
            if serializer.is_valid():
                action = serializer.save()
                return Response({"Action Created": ActionSerializer(action).data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create Event Member who is Following
class CreateFollowEventMemberView(APIView):
    def post(self, request, format='json'):
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        event_id = int(request.POST.get('event'))
        if event_id:
            serializer = FollowEventMemberSerializer(data=request_data)
            if serializer.is_valid():
                member = serializer.save()
                return Response({"Event Member Created which is Following": FollowEventMemberSerializer(member).data},
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create Event Member who is not Following
class CreateUnfollowEventMemberView(APIView):
    def post(self, request, format='json'):
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        event_id = int(request.POST.get('event'))
        if event_id:
            check_member = EventMember.objects.filter(event_id=event_id, user=request.user).first()
            if not check_member:
                serializer = UnfollowEventMemberSerializer(data=request_data)
                if serializer.is_valid():
                    member = serializer.save()
                    return Response(
                        {"Event Member Created which is not Following": UnfollowEventMemberSerializer(member).data},
                        status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Member Already Exists'}, status=status.HTTP_400_BAD_REQUEST)


# Add Event Member API
class AddEventMemberView(APIView):
    def post(self, request, format='json'):
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        event_id = int(request.POST.get('event'))
        if event_id:
            member = EventMember.objects.filter(event_id=event_id, user=request.user).first()
            if not member:
                serializer = AddEventMemberSerializer(data=request_data)
                # import pdb;pdb.set_trace()
                if serializer.is_valid():
                    add_member = serializer.save()
                    return Response({"Event Member Added": AddEventMemberSerializer(add_member).data},
                                    status=status.HTTP_201_CREATED)
            else:
                return Response("Member Already Exists")


# Remove Event Member API
class RemoveEventMemberView(APIView):
    def post(self, request, format='json'):
        user_id = request.user.id
        event_id = request.POST.get('event')
        if event_id:
            resp = remove_event_member(event_id=event_id, user_id=user_id)
            return Response(resp, status=status.HTTP_200_OK)


# Get User All Events
class UserEventView(APIView):
    # permission_classes = (AllowAny,)
    def get(self, request):
        user_id = request.user.id
        resp = {"data": get_user_event(user_id=user_id)}
        return Response(data=resp, status=status.HTTP_200_OK)


# Get all comments on a certain Event
class CommentEventView(APIView):
    def get(self, request):
        user_id = request.user.id
        event_id = request.GET.get('event_id', 1)
        resp = {"data": get_event_comments(event_id=event_id, user_id=user_id)}
        return Response(data=resp, status=status.HTTP_200_OK)


# Get all actions submitted on a certain event
class EventActionView(APIView):
    def get(self, request):
        user_id = request.user.id
        event_id = request.GET.get('event_id', 1)
        resp = {"data": get_event_actions(event_id=event_id, user_id=user_id)}
        return Response(data=resp, status=status.HTTP_200_OK)


# Get All Events those are Following
class FollowEventView(APIView):
    def get(self, request):
        user_id = request.user.id
        follow = request.GET.get('follow', True)
        resp = {"data": get_follow_events(follow=follow, user_id=user_id)}
        return Response(data=resp, status=status.HTTP_200_OK)


# Get All Events those are not Following
class UnfollowEventView(APIView):
    def get(self, request):
        user_id = request.user.id
        follow = request.GET.get('follow', False)
        resp = {"data": get_unfollow_events(follow=follow, user_id=user_id)}
        return Response(data=resp, status=status.HTTP_200_OK)


class ImportContacts(APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        dict_list = request.data
        users = request.user.ref_user.all()
        for item in dict_list:
            email = item['email']
            friend = User.objects.filter(email=email).first()
            if friend and friend not in users:
                request.user.ref_user.add(friend)
            elif not friend:
                data = {"email": email, "password": "123456789"}
                serializer = TemporaryUserSerializer(data=data)
                if serializer.is_valid():
                    User.temporary_profile = True
                    serializer.save()
                return Response("Temporary User Created.", status=status.HTTP_201_CREATED)
