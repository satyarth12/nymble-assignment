from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Store, Items, TransactionBill

import concurrent.futures


class StoreSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Store
        fields = '__all__'

    def get_owner(self, obj):
        owner = obj.owner
        owner_details = {
            'id': str(owner.id),
            'username': str(owner.username)
        }
        return owner_details


class ItemsSerializer(serializers.ModelSerializer):
    store = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Items
        fields = '__all__'

    def get_store(self, obj):
        store_serializer = StoreSerializer(obj.store, many=False)
        return store_serializer.data


class TransactionBillSerializer(serializers.ModelSerializer):
    total_items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TransactionBill
        fields = '__all__'
        read_only_fields = ['total_items']

    def get_recipient(self, obj):
        recipient = obj.recipient
        recipient_details = {
            'id': str(recipient.id),
            'username': str(recipient.username)
        }
        return recipient_details

    def get_items(self, obj):
        items_serializer = ItemsSerializer(obj.items, many=True)
        return items_serializer.data

    def get_total_items(self, obj):
        return len(obj.cart)

    #     # print(items[0].transaction_items.all())
