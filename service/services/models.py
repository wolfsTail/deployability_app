from django.db import models
from django.core.validators import MaxValueValidator

from clients.models import Client


class Service(models.Model):
    name = models.CharField(max_length=64)
    full_price = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f"Service: {self.name}"


class Plan(models.Model):
    PLAN_TYPES = (("full", "Full"), ("student", "Student"), ("discount", "Discount"))

    plan_type = models.CharField(choices=PLAN_TYPES, max_length=8)
    discount_percent = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(100)]
    )

    def __str__(self) -> str:
        return f"Plan: {self.plan_type}, {self.discount_percent}"


class Subscription(models.Model):
    client = models.ForeignKey(
        Client, related_name="subscriptions", on_delete=models.PROTECT
    )
    service = models.ForeignKey(
        Service, related_name="subscriptions", on_delete=models.PROTECT
    )
    plan = models.ForeignKey(
        Plan, related_name="subscriptions", on_delete=models.PROTECT
    )

    def __str__(self) -> str:
        return f"Subscription: {self.client}, {self.service}, {self.plan}"
