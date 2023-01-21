from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CustomUser(AbstractUser):

    class Status(models.TextChoices):
        s1 = 'AR', _('Architekt')
        s2 = 'INW', _('Inwestor')
        s3 = 'GW', _('Generalny Wykonawca')
        s4 = 'INI', _('Inspektor Nadzoru Inwestorskiego')

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.s2)

    def __str__(self):
        return self.username