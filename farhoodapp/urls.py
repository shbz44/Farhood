from django.conf.urls import url
from farhoodapp.views import (UserCreate, CreateProfileUser, UserEventView, EventCreateView, EventEditView,
                              CommentEventView, CreateCommentView, CreateActionView, CreateFollowEventMemberView,
                              EventActionView, RemoveEventMemberView, AddEventMemberView, CreateUnfollowEventMemberView,
                              FollowEventView, UnfollowEventView, ImportContacts)

from django.conf import settings
from django.conf.urls.static import static

from . import views as local_views
from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
                  # url(r'^login/$', local_views.get_auth_token, name='login'),
                  # url(r'^logout/$', local_views.logout_user, name='logout'),
                  # url(r'^auth/$', local_views.login_form, name='login_form'),
                  url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),

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

                  # Create Action API
                  url(r'^action/create/$', CreateActionView.as_view()),

                  # Create Event Member who is Following
                  url(r'^follow/member/$', CreateFollowEventMemberView.as_view()),

                  # Remove Event Member API
                  url(r'^remove/member/$', RemoveEventMemberView.as_view()),

                  # Add Event Member API
                  url(r'^add/member/$', AddEventMemberView.as_view()),

                  # Create Event Member who is not Following
                  url(r'^unfollow/member/$', CreateUnfollowEventMemberView.as_view()),

                  # Get All Events those are Following
                  url(r'^follow/event/$', FollowEventView.as_view()),

                  # Get All Events those are not Following
                  url(r'^unfollow/event/$', UnfollowEventView.as_view()),

                  # Get all comments on a certain Event
                  url(r'^comment/$', CommentEventView.as_view()),

                  # Get all actions submitted on a certain even
                  url(r'^action/event/$', EventActionView.as_view()),

                  # Get User All Events
                  url(r'^user/event/$', UserEventView.as_view()),

                  url(r'^contacts/$', ImportContacts.as_view()),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
