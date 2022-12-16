from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, 
                                        PermissionsMixin)
from django.utils.translation import gettext_lazy
from django.utils import timezone

from .managers import PDFUserManager


class Role (models.Model):
    STUDENT = 1
    FACULTY = 2

    ROLE_CHOICES = (
        (STUDENT, 'student'),
        (FACULTY, 'faculty')
    )

    rolesId = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self.get_id_display()

# PDF BASE USER: USER MODEL WHICH HANDLES ALL THE MODELS FOR ANY KIND OF USERS.

class PDFBaseUser(AbstractBaseUser, PermissionsMixin):
    userId = models.CharField(max_length=150, unique=True)
    email = models.EmailField(gettext_lazy('email address'), unique=True)
    studentNumber = models.CharField(max_length=7, null=False)
    firstName = models.CharField(max_length=255, null=False)
    middleName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255, null=False)
    roles = models.ManyToManyField(Role)
    dateJoined = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = PDFUserManager()

    USERNAME_FIELD = 'userId'
    REQUIRED_FIELDS = ['email', 'firstName', 'lastName', ]

    def __str__(self):
        return self.userId

    def detailName(self):
        return self.firstName + ' ' + self.lastName

    def as_dict(self):
        context = {
            'id' : self.id,
            'fullName' : self.firstName + ' ' + self.lastName,
        }
        return context




