from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


def validate_phone_number(value):
    if ((len(value) < 11) or (len(value) > 14)):
        raise Exception(_('phone number must be 11 characters.'))
    
    if value[0] == '0':
        pass
    elif value[0] == '9':
        value = '0' + value
    
    return value

class User(AbstractUser):
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=20,
        unique=False,
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        verbose_name=_("First name"),
        max_length=35,
        null=False,
        blank=False,
    )
    last_name = models.CharField(
        verbose_name=_("Last name"),
        max_length=35,
        null=False,
        blank=False,
    )
    phone_number = PhoneNumberField(
        verbose_name=_("Phone number"),
        unique=True,
        validators=[validate_phone_number]
    )
    email = models.EmailField(
        verbose_name=_("Email address"),
        unique=True,
    )
    password = models.CharField(
        verbose_name=_("Password"),
        max_length=225,
        blank=False,
    )
    
    USERNAME_FIELD = "phone_number"

    def get_username(self) -> str:
        return str(self.phone_number)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
