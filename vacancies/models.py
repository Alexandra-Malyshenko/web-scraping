from django.db import models
from django.conf import settings
# Create your models here.


class Vacancy(models.Model):

    title = models.CharField(max_length=250)
    url = models.TextField()
    company = models.CharField(max_length=50)
    city = models.CharField(max_length=250)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    last_scape = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{}-{}".format(self.user, self.last_scape)

