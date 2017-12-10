from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    image = models.ImageField(upload_to='images/', null=True)
    email = models.EmailField(unique=True)
    first_name =  models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    nick_name = models.CharField(max_length=150)
    username = models.CharField(max_length=50, unique=True)
    account_id = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=150)
    temporary_profile = models.BooleanField(default=True)
    ref_user = models.ManyToManyField('self', blank=True)

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


class Event(models.Model):
    COFFEE = 'coffee'
    BEAR = 'bear'
    SHOPPINGS = 'shopping'
    DINNING = 'dinning'
    LOGO = 'logo'
    SPORTS = 'sports'

    TYPE_CHOICES = (
        (COFFEE, 'Coffee'),
        (BEAR, 'Bear'),
        (SHOPPINGS, 'Shopping'),
        (DINNING, 'Dinning'),
        (LOGO, 'Logo'),
        (SPORTS, 'Sports')
    )
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=150, choices=TYPE_CHOICES, default=COFFEE)
    description = models.CharField(max_length=150)
    scheduled_time = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # Or we can make it Float Field
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # Or we can make it Float Field
    location_name = models.CharField(max_length=150)
    location_address = models.CharField(max_length=200)


class Comment(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    message = models.CharField(max_length=200)


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


class EventMember(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    follow = models.BooleanField(default=False)
