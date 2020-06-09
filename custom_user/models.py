import uuid

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password, user_type, *args, **kwargs):
        if not email:
            raise ValueError(_("Email address must be provided"))
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.user_type = user_type
        user.save()
        return user

    def create_superuser(self, email, password, user_type=3, *args, **kwargs):
        user = self.create_user(email=email, password=password, user_type=user_type)
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    WORKER = 1
    MANAGER = 2
    DEVELOPER = 3
    USER_TYPE_CHOICES = (
        (WORKER, "customer"),
        (MANAGER, "celebrity"),
        (DEVELOPER, "developer"),
    )

    email = models.EmailField(verbose_name=_("Email Address"), unique=True)
    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES, blank=False, null=False
    )
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(verbose_name="First name", max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    jwt_secret = models.UUIDField(default=uuid.uuid4)
    date_joined = models.DateTimeField(verbose_name=_("Joined on"), auto_now_add=True, db_index=True)

    objects = UserManager()

    REQUIRED_FIELDS = ["user_type"]

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_first_name(self):
        return self.first_name

    def get_email(self):
        return self.email

    def get_phone(self):
        if self.user_type == 3:
            return ""
        else:
            return str(self.phone_number)

    def get_user_type(self):
        """Returns a string containing the user_type"""
        for id, user_type_str in User.USER_TYPE_CHOICES:
            if id == self.user_type:
                return user_type_str


    def save(self, *args, **kwargs):
        if self.user_type == User.DEVELOPER:
            self.is_admin = True
        super().save(*args, **kwargs)


def jwt_get_secret_key(user_model):
    return user_model.jwt_secret