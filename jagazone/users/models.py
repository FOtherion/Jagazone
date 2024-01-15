import uuid
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    """
    Default custom user model for Jagazone.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore


    class Meta:
        ordering = ('name',)
        get_latest_by = 'name'

    def __str__(self) -> str:
        return f'<User ID: {self.id}>'

    @property
    def user_profile(self):
        return self.usersprofile

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Gender(models.TextChoices):
        male = 'Male'
        female = 'Female'
        other = 'Other'


class UsersProfile(models.Model):
    GUEST = 'GU'
    ADMIN = 'AD'
    N_CONFIRMED = 'NU'
    CONFIRMED = 'CU'

    ROLE_CHOICES = [
        (GUEST, 'Gues'),
        (ADMIN, 'Admin'),
        (N_CONFIRMED, 'Not confirmed user'),
        (CONFIRMED, 'Confirmed User'),
    ]

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(blank=True)
    role = CharField(max_length=2,
                    choices=ROLE_CHOICES,
                    default='GU',
                    )
    gender = CharField(max_length=15,
                        choices=Gender.choices,
                        default=Gender.other.other,
                        )
    created = models.DateTimeField(auto_now_add=True)
    archived = models.DateTimeField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=25, blank=True)
    confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)
        get_latest_by = 'created'

    def __str__(self) -> str:
        return f'<UserProfile ID: {self.id}>'

    def age(self):
        if self.birthdate:
            return timezone.now().year - self.birthdate.year

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


