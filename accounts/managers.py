from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy

class PDFUserManager(BaseUserManager):
    def create_user(self, userId, email, firstName, password, **other_fields):

        if not email:
            raise ValueError(gettext_lazy('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(userId=userId, email=email, firstName=firstName, **other_fields)
        user.set_password(password)
        user.save()
        
        return user

    def create_superuser(self, userId, email, firstName, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        
        return self.create_user(userId, email, firstName, password, **other_fields)

