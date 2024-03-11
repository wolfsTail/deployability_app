from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    company_name = models.CharField(max_length=128)
    curr_address = models.CharField(max_length=128)

    def __str__(self):
        return f"Client: {self.company_name}"
