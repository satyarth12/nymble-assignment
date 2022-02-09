from unicodedata import name
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import ItemCategory, Store, Items, TransactionBill


class UserSerializer(serializers.ModelSerializer):
    store_meta_details = serializers.SerializerMethodField(read_only=True)
    items_meta_details = serializers.SerializerMethodField(read_only=True)
    food_category_meta_details = serializers.SerializerMethodField(
        read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email",
                  "store_meta_details", "items_meta_details", "food_category_meta_details"]
        read_only_fields = ["id", "username", "email",
                            "store_meta_details", "items_meta_details", "food_category_meta_details"]

    def get_store_meta_details(self, obj):
        store = obj.store_owner

        all_store_transactions = TransactionBill.objects.filter(
            store=store, placed=True)  # .count()

        total_item_quant_sold = 0
        total_sales_amt = 0
        for ins in all_store_transactions:
            total_item_quant_sold += len(ins.cart)
            total_sales_amt += float(ins.total)

        return{
            "store_name": str(store),
            "total_transactions": all_store_transactions.count(),
            "total_quantity_items_sold": total_item_quant_sold,
            "total_sales_amount": total_sales_amt
        }

    def get_items_meta_details(self, obj):
        items = obj.store_owner.item_store.all()
        sub_result = {}
        for item in items:
            sub_result[str(item.name)] = item.transaction_items.count()
        return sub_result

    def get_food_category_meta_details(self, obj):
        categories = ItemCategory.objects.all()
        result = {}
        for cat in categories:
            result[str(cat.name)] = cat.item_in_category.count()
        return result


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
    quantity_sold = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Items
        fields = '__all__'

    def get_store(self, obj):
        store_serializer = StoreSerializer(obj.store, many=False)
        return store_serializer.data

    def get_quantity_sold(self, obj):
        pass


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
        items_serializer = ItemsSerializer(obj.cart.keys(), many=True)
        return items_serializer.data

    def get_total_items(self, obj):
        return len(obj.cart)

    #     # print(items[0].transaction_items.all())
