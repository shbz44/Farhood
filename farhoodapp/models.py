from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


def upload_profile_image(instance, filename):
    user = User.objects.get(id=instance.id)
    return '{}/{}/{}'.format("Users", user.id, 'profile_image.jpg')


class User(AbstractBaseUser):
    image = models.ImageField(upload_to=upload_profile_image, blank=True, null=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    nick_name = models.CharField(max_length=150, null=True, blank=True)
    username = models.CharField(max_length=50)
    account_id = models.CharField(max_length=10, null=True, blank=True)
    phone_number = models.CharField(max_length=150, null=True, blank=True)
    temporary_profile = models.BooleanField(default=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    ref_user = models.ManyToManyField('self', null=True)

    is_staff = models.BooleanField(
        ('staff status'),
        default=False,
        help_text=('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        ('active'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_superuser = models.BooleanField(
        ('superuser'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as super user or not . '
            'Unselect this instead of deleting accounts.'
        ),
    )

    has_perm = models.BooleanField(
        ('perm'),
        default=True,
        help_text=(
            'Designates whether this user should be treated as super user or not . '
            'Unselect this instead of deleting accounts.'
        ),
    )

    def has_perm(self, arg):
        if self.is_superuser:
            return True
        return False

    def get_short_name(self):
        return self.email

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return str(self.id)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Event(models.Model):
    COFFEE = 'coffee'
    BEER = 'beer'
    SHOPPINGS = 'shopping'
    DINNING = 'dinning'
    LOGO = 'logo'
    SPORTS = 'sports'

    EVENT_TYPE = (
        (COFFEE, 'Coffee'),
        (BEER, 'Beer'),
        (SHOPPINGS, 'Shopping'),
        (DINNING, 'Dinning'),
        (LOGO, 'Logo'),
        (SPORTS, 'Sports')
    )
    name = models.CharField(max_length=150)
    event_type = models.CharField(max_length=150, choices=EVENT_TYPE, default=COFFEE)
    description = models.CharField(max_length=150)
    scheduled_time = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    longitude = models.FloatField(null=True, blank=True, default=0.0)
    latitude = models.FloatField(null=True, blank=True, default=0.0)
    location_name = models.CharField(max_length=150)
    location_address = models.CharField(max_length=200)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    message = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)


class Action(models.Model):
    GOOD = 'good'
    BAD = 'bad'
    WORST = 'worst'

    ACTION_TYPE = (
        (GOOD, 'Good'),
        (BAD, 'Bad'),
        (WORST, 'Worst')
    )
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    action_type = models.CharField(max_length=150, choices=ACTION_TYPE, default=GOOD)

    def __str__(self):
        return str(self.id)


class EventMember(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    follow = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
