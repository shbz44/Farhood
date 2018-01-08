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
                                 get_unfollow_events, remove_event_member, get_contact_list, get_user_profile,
                                 get_user_image_url)
from farhoodapp.utils.all_responses import CustomResponse


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
            return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", UserSerializer(user).data)
        return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, str(serializer.errors))


class LogoutView(APIView):
    queryset = User.objects.all()

    def get(self, request):
        request.user.auth_token.delete()
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Logout Successfully", {})


# Create Profile API
class CreateProfileUser(APIView):
    def put(self, request, format='json'):
        user_data = request.user
        request_data = request.data.copy()
        request_data['is_active'] = True
        serializer = UserSerializer(user_data, data=request_data)
        if serializer.is_valid():
            user = serializer.save()
            return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", UserSerializer(user).data)
        return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, str(serializer.errors))


class GetUserProfileView(APIView):
    def get(self, request):
        id = request.user.id
        resp = get_user_profile(id=id, request=request)
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", resp)


class UserImageView(APIView):
    def get(self, request):
        id = request.user.id
        resp = get_user_image_url(id=id, request=request)
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", resp)


# Create Event API
class EventCreateView(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, format='json'):
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        serializer = EventSerializer(data=request_data)
        if serializer.is_valid():
            event = serializer.save()
            return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", EventSerializer(event).data)
        return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, str(serializer.errors))


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
            return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", EventSerializer(event).data)
        return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, str(serializer.errors))


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
                return CustomResponse.create_response(True, status.HTTP_200_OK, "Success",
                                                      CommentSerializer(comment).data)
            return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, str(serializer.errors))


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
                return CustomResponse.create_response(True, status.HTTP_200_OK, "Success",
                                                      ActionSerializer(action).data)
            return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, str(serializer.errors))


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
                return CustomResponse.create_response(True, status.HTTP_200_OK, "Success",
                                                      FollowEventMemberSerializer(member).data)
            return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, str(serializer.errors))


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
                    return CustomResponse.create_response(True, status.HTTP_200_OK, "Success",
                                                          UnfollowEventMemberSerializer(member).data)
            else:
                return Response({'error': 'Member Already Exists'}, status=status.HTTP_400_BAD_REQUEST)


# Add Event Member APIa
class AddEventMemberView(APIView):
    def post(self, request, format='json'):
        request_data = request.data.copy()
        request_data['user'] = request.user.id
        event_id = int(request.POST.get('event'))
        if event_id:
            member = EventMember.objects.filter(event_id=event_id, user=request.user).first()
            if not member:
                serializer = AddEventMemberSerializer(data=request_data)
                if serializer.is_valid():
                    add_member = serializer.save()
                    return CustomResponse.create_response(True, status.HTTP_200_OK, "Success",
                                                          AddEventMemberSerializer(add_member).data)
            else:
                return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, "")  # str(serializer.errors))


# Remove Event Member API
class RemoveEventMemberView(APIView):
    def post(self, request, format='json'):
        user_id = request.user.id
        event_id = request.POST.get('event')
        if event_id:
            resp = remove_event_member(event_id=event_id, user_id=user_id)
            return CustomResponse.create_response(True, status.HTTP_200_OK, "Event Member Removed", resp)


# Get User All Events
class UserEventView(APIView):
    def get(self, request):
        user_id = request.user.id
        resp = get_user_event(user_id=user_id)
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", resp)


# Get all comments on a certain Event
class CommentEventView(APIView):
    def get(self, request):
        user_id = request.user.id
        event_id = request.GET.get('event_id', 1)
        resp = get_event_comments(event_id=event_id, user_id=user_id)
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", resp)


# Get all actions submitted on a certain event
class EventActionView(APIView):
    def get(self, request):
        user_id = request.user.id
        event_id = request.GET.get('event_id', 1)
        resp = get_event_actions(event_id=event_id, user_id=user_id)
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", resp)


# Get All Events those are Following
class FollowEventView(APIView):
    def get(self, request):
        user_id = request.user.id
        follow = request.GET.get('follow', True)
        resp = get_follow_events(follow=follow, user_id=user_id)
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", resp)


# Get All Events those are not Following
class UnfollowEventView(APIView):
    def get(self, request):
        user_id = request.user.id
        follow = request.GET.get('follow', False)
        resp = get_unfollow_events(follow=follow, user_id=user_id)
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", resp)


class ImportContacts(APIView):
    parser_classes = (JSONParser,)

    def post(self, request):
        dict_list = request.data
        users = request.user.ref_user.all()
        for item in dict_list:
            email = item.get('email')
            friend = User.objects.filter(email=email).first()
            if friend and friend not in users:
                request.user.ref_user.add(friend)
            elif not friend:
                data = {"email": email, "password": "123456789"}
                serializer = TemporaryUserSerializer(data=data)
                if serializer.is_valid():
                    User.temporary_profile = True
                    serializer.save()
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", {})
        # return CustomResponse.create_error_response(status.HTTP_400_BAD_REQUEST, "")


class ContactsView(APIView):
    def get(self, request):
        id = request.user.id
        resp = get_contact_list(id=id)
        return CustomResponse.create_response(True, status.HTTP_200_OK, "Success", resp)
