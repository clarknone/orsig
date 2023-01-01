import os
import secrets
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import validate_email
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Create your models here.
from django.utils.timezone import now

from orsig.helpers.generators import Generator


def get_avatar_path(instance, filename):
    filename, file_extension = os.path.splitext(filename)
    return "userfiles/%s/avatar/%s.%s" % (instance.hash, secrets.token_hex(32), file_extension)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not (email and password):
            raise ValueError('required field not found')
        user = self.model(email=email.lower(), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('type', 5)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.PositiveIntegerField(default=Generator.generate_pk, primary_key=True)
    email = models.EmailField(max_length=127, unique=True, validators=[validate_email])
    full_name = models.CharField(default='', blank=True, max_length=32)
    phone = models.CharField(max_length=32, blank=True, default=None, null=True)
    avatar = models.ImageField(upload_to=get_avatar_path, null=True, default=None, blank=True, max_length=256)
    bio = models.CharField(max_length=256, default='', blank=True)
    type = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=now, blank=True)
    last_login = models.DateTimeField(default=None, null=True, blank=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Admin:
        list_display = ('email', 'full_name', 'date_created', 'last_login')
        search_fields = ('email__icontains',)
