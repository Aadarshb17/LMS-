from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Admin(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10, blank=False)

    def __str__(self):
        return f" User- {self.user_id}"
