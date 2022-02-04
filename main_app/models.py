from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

import uuid

USER = get_user_model()

# Create your models here.


class Store(models.Model):
    owner = models.ForeignKey(
        USER, related_name="store_owner", on_delete=models.CASCADE)

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


class TransactionBill(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    timestamp = models.DateTimeField()

    recipient = models.ForeignKey(
        USER, related_name="transaction_recipient", on_delete=models.DO_NOTHING)

    items = models.ManyToManyField(
        Items, related_name="transaction_items")
    cart = models.JSONField(null=True)
    total = models.FloatField(
        _("Total Transaction Amount"), default=0)

    class Meta:
        app_label = 'main_app'
        verbose_name = 'Transaction Bill'
        verbose_name_plural = 'Transaction Bills'

    def __str__(self):
        return f"{self.recipient.username}"
