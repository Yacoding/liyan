# -*- coding: utf-8 -*-
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.utils import timezone
# import django_databrowse

class UserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email or not username or not password:
            raise ValueError('Users must have an email address, a username and a password')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            create_time=timezone.now(),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        u = self.create_user(username, email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser):
    username = models.CharField(max_length=200, db_index=True, verbose_name='username')
    email = models.EmailField(max_length=200, unique=True, db_index=True, verbose_name='email')
    create_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    active_code = models.CharField(max_length=500)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.username + "-" + self.email

# django_databrowse.site.register(User)