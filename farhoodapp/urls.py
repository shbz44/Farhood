from django.conf.urls import url
from farhoodapp.views import (UserCreate, CreateProfileUser, UserEventView, EventCreateView, EventEditView,
                              CommentEventView, CreateCommentView, CreateActionView, CreateFollowEventMemberView,
                              EventActionView, RemoveEventMemberView, AddEventMemberView, CreateUnfollowEventMemberView,
                              FollowEventView, UnfollowEventView)

urlpatterns = [
    # SignUp API
    url(r'^user/create/$', UserCreate.as_view()),

    # Create Profile API
    url(r'^profile/$', CreateProfileUser.as_view()),

    # Create Event API
    url(r'^event/create/$', EventCreateView.as_view()),

    # Edit Event API
    url(r'^edit/event/$', EventEditView.as_view()),

    # Create Comment View
    url(r'^create/comment/$', CreateCommentView.as_view()),

    #Create Action API
    url(r'^action/create/$', CreateActionView.as_view()),

    #Create Event Member who is Following
    url(r'^follow/member/$', CreateFollowEventMemberView.as_view()),

    #Remove Event Member API
    url(r'^remove/member/$', RemoveEventMemberView.as_view()),

    #Add Event Member API
    url(r'^add/member/$', AddEventMemberView.as_view()),

    #Create Event Member who is not Following
    url(r'^unfollow/member/$', CreateUnfollowEventMemberView.as_view()),

    #Get All Events those are Following
    url(r'^follow/event/$', FollowEventView.as_view()),

    # Get All Events those are not Following
    url(r'^unfollow/event/$', UnfollowEventView.as_view()),

    #Get all comments on a certain Event
    url(r'^comment/$', CommentEventView.as_view()),

    #Get all actions submitted on a certain even
    url(r'^action/event/$', EventActionView.as_view()),

    #Get User All Events
    url(r'^user/event/$', UserEventView.as_view()),

]
