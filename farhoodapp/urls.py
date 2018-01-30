from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as rest_framework_views
from farhoodapp.views import (UserCreate, CreateProfileUser, UserEventView, EventCreateView, EventEditView,
                              CommentEventView, CreateCommentView, CreateActionView, CreateFollowEventMemberView,
                              EventActionView, RemoveEventMemberView, AddEventMemberView, CreateUnfollowEventMemberView,
                              FollowEventView, UnfollowEventView, ImportContacts, ContactsView, GetUserProfileView,
                              UserImageView, LogoutView, UnfollowFriends, FollowFriends, )

urlpatterns = [
                  url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
                  url(r'^user/create/$', UserCreate.as_view()),
                  url(r'^profile/$', CreateProfileUser.as_view()),
                  url(r'^event/create/$', EventCreateView.as_view()),
                  url(r'^edit/event/$', EventEditView.as_view()),
                  url(r'^create/comment/$', CreateCommentView.as_view()),
                  url(r'^action/create/$', CreateActionView.as_view()),
                  url(r'^add/member/$', AddEventMemberView.as_view()),
                  url(r'^follow/member/$', CreateFollowEventMemberView.as_view()),
                  url(r'^unfollow/member/$', CreateUnfollowEventMemberView.as_view()),
                  url(r'^contacts/$', ImportContacts.as_view()),
                  url(r'^friend/unfollow/$', UnfollowFriends.as_view()),
                  url(r'^friend/follow/$', FollowFriends.as_view()),
                  url(r'^remove/member/$', RemoveEventMemberView.as_view()),
                  url(r'^follow/event/$', FollowEventView.as_view()),
                  url(r'^unfollow/event/$', UnfollowEventView.as_view()),
                  url(r'^comment/$', CommentEventView.as_view()),
                  url(r'^action/event/$', EventActionView.as_view()),
                  url(r'^user/event/$', UserEventView.as_view()),
                  url(r'^get/contacts/$', ContactsView.as_view()),
                  url(r'^get/profile/$', GetUserProfileView.as_view()),
                  url(r'^image/', UserImageView.as_view()),
                  url(r'^logout/', LogoutView.as_view()),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)