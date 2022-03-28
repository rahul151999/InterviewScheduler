from datetime import date

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token

from InterviewScheduler import settings


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    first_name = None
    last_name = None
    user_name = None
    name = models.CharField('name', max_length=150, blank=True)
    email = models.EmailField('email address', blank=True, error_messages={
        'unique': "A user with that email already exists.",
    }, unique=True)
    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_interviewer = models.BooleanField(
        'is interviewer',
        default=False,
        help_text='Check whether the user in interviewer or not',
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)
    is_deleted = models.BooleanField('is deleted', default=False)
    updated_at = models.DateTimeField('updated date', default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        if instance.is_superuser:
            Token.objects.create(user=instance, key="superuser_key")
        else:
            Token.objects.create(user=instance)  # use generated key


class InterviewerAvailability(models.Model):
    """
    Contains interviewer available time.
    """
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interviewer')
    interview_date = models.DateField("interview_date", default=date.today)
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')

    def __str__(self):
        return self.interviewer.name


class CandidateAvailability(models.Model):
    """
    Contains Candidate available time.
    """
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name='candidate')
    interview_date = models.DateField("interview_date", default=date.today)
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')

    def __str__(self):
        return self.candidate.name
