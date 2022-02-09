from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

import uuid

from .exceptions import ItemUnavailableError
# Create your models here.


class Store(models.Model):
    owner = models.ForeignKey(
        User, related_name="store_owner", on_delete=models.CASCADE)

    name = models.CharField(_("Store Name"), primary_key=True, max_length=250)
    created_at = models.DateField(
        _("Store's operating day"), auto_now_add=True)

    class Meta:
        app_label = 'main_app'
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'

    def __str__(self):
        return self.name


class Items(models.Model):

    class Types(models.TextChoices):
        """Item type choices
        """
        PIZZA = "PIZZA", "pizza"
        BURGER = "BURGER", "burger"

    store = models.ForeignKey(
        Store, on_delete=models.DO_NOTHING, related_name="item_store")
    name = models.CharField(_("Item Name"), blank=True, max_length=250)
    code = models.CharField(_("Item Code"), blank=True, max_length=50)
    price = models.FloatField(_("Item Price"), blank=True)
    quantity = models.IntegerField(_("Available Quantity"), default=50)
    type = models.CharField(
        _("Item Type"), max_length=50, choices=Types.choices,
    )

    class Meta:
        app_label = 'main_app'
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return f"{self.store} - {self.name}"

    @staticmethod
    def reduce_quantity(instance):
        if instance.quantity > 0:
            instance.quantity = instance.quantity-1
            return instance.save()
        raise ItemUnavailableError


class TransactionBill(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    recipient = models.ForeignKey(
        User, related_name="transaction_recipient", on_delete=models.DO_NOTHING, null=True)

    store = models.ForeignKey(
        Store, related_name='transaction_store', on_delete=models.DO_NOTHING, null=True)
    # items = models.ManyToManyField(
    #     Items, related_name="transaction_items")
    cart = models.JSONField(null=True, default=dict)
    total = models.FloatField(
        _("Total Transaction Amount"), default=0)

    placed = models.BooleanField(default=False)

    class Meta:
        app_label = 'main_app'
        verbose_name = 'Transaction Bill'
        verbose_name_plural = 'Transaction Bills'

    def __str__(self):
        return f"{self.id}"
