# from django.conf import settings
# from django.contrib.auth.hashers import check_password
# from django.contrib.auth.models import User
#
# class SettingsBackend:
#     """
#     Authenticate against the settings ADMIN_LOGIN and ADMIN_PASSWORD.
#
#     Use the login name and a hash of the password. For example:
#
#     ADMIN_LOGIN = 'admin'
#     ADMIN_PASSWORD = 'pbkdf2_sha256$30000$Vo0VlMnkR4Bk$qEvtdyZRWTcOsCnI/oQ7fVOu1XAURIZYoOZ3iq8Dr4M='
#     """
#
#     def authenticate(self, request, username=None, password=None):
#         login_valid = (settings.ADMIN_LOGIN == username)
#         pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
#         if login_valid and pwd_valid:
#             try:
#                 user = User.objects.get(email=username)
#             except User.DoesNotExist:
#                 # Create a new user. There's no need to set a password
#                 # because only the password from settings.py is checked.
#                 user = User(username=username)
#                 user.is_staff = True
#                 user.is_superuser = True
#                 user.save()
#             return user
#         return None
#
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None
from django.contrib.auth.hashers import check_password
from farhoodapp.models import User

class LoginUsingEmailAsUsernameBackend(object):
  """
  Custom Authentication backend that supports using an e-mail address
  to login instead of a username.
  See: http://blog.cingusoft.org/custom-django-authentication-backend
  """
  supports_object_permissions = False
  supports_anonymous_user = False
  supports_inactive_user = False

  def authenticate(self, username=None, password=None):
    try:
      # Check if the user exists in Django's database
      user = User.objects.get(email=username)
    except User.DoesNotExist:
      return None

    # Check password of the user we found
    if check_password(password, user.password):
      return user
    return None

  # Required for the backend to work properly - unchanged in most scenarios
  def get_user(self, user_id):
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None