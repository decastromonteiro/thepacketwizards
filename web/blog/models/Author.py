from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def get_name(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    def __str__(self):
        return self.get_name()
