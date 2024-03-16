from django.db import models
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_delete

from clients.models import Client
from services.tasks import set_price, set_comment
from services.receivers import delete_cache_total_sum


class Service(models.Model):
    name = models.CharField(max_length=64)
    full_price = models.PositiveIntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__full_price = self.full_price

    def save(self, *args, **kwargs):

        if self.__full_price != self.full_price:
            for subcription in self.subscriptions.all():
                set_comment.delay(subcription.id)                
                set_price.delay(subcription.id)

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Service: {self.name}"


class Plan(models.Model):
    PLAN_TYPES = (("full", "Full"), ("student", "Student"), ("discount", "Discount"))

    plan_type = models.CharField(choices=PLAN_TYPES, max_length=8)
    discount_percent = models.PositiveIntegerField(
        default=0, validators=[MaxValueValidator(100)]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__discount_percent = self.discount_percent

    def save(self, *args, **kwargs):

        if self.discount_percent != self.__discount_percent:
            for subcription in self.subscriptions.all():
                set_price.delay(subcription.id)
                set_comment.delay(subcription.id)

        return super().save(*args, **kwargs)

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
    price = models.PositiveIntegerField(default=0)
    comment = models.CharField(max_length=128, null=True, blank=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["client", "service"])
        ]

    def save(self, *args, **kwargs):
        creating = not bool(self.id)
        result = super().save(*args, **kwargs)

        # if creating:
        #     set_price.delay(self.id)

        return result

    def __str__(self) -> str:
        return f"Subscription: {self.client}, {self.service}, {self.plan}"


post_delete.connect(delete_cache_total_sum, sender=Subscription)
