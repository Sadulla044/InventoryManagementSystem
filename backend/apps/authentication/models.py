from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from django.utils import timezone

from .managers import CustomUserManager


class Users(AbstractBaseUser, PermissionsMixin):
    GENDER_TYPES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('rns', 'Rather not say')
    )

    first_name = models.CharField(
        verbose_name='First name',
        max_length=50
    )
    last_name = models.CharField(
        verbose_name='Last name',
        max_length=50,
        null=True, blank=True
    )
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True
    )
    password = models.CharField(
        verbose_name='Password',
        max_length=255
    )
    birth_date = models.DateField(
        verbose_name='Date of birth'
    )
    gender = models.CharField(
        verbose_name='Gender',
        max_length=10,
        choices=GENDER_TYPES
    )

    is_staff = models.BooleanField(
        verbose_name='Staff status',
        default=False
    )
    is_active = models.BooleanField(
        verbose_name='Active user',
        default=True
    )
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'password',
        'birth_date',
        'gender'
    ]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        app_label = 'authentication'
        db_table = 'Users'
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}' if self.last_name else self.first_name
