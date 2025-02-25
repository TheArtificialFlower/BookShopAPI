from rest_framework import serializers
from .models import Book, Order, OrderItems, Coupons
from django.utils.timezone import now

class BookSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(read_only=True, slug_field="name")
    class Meta:
        model = Book
        fields = "__all__"

    def get_likes(self, obj):
        return obj.likes.count()



class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class OrderItemsSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    class Meta:
        model = OrderItems
        fields = "__all__"

    def get_total(self, obj):
        return obj.get_cost()


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_items(self, obj):
        result = obj.items.all()
        return OrderItemsSerializer(instance=result, many=True).data

    def get_total(self, obj):
        return obj.get_total_price()


class CartItemSerializer(serializers.Serializer):
    book = serializers.DictField(child=serializers.CharField())
    quantity = serializers.IntegerField()

class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    total_price = serializers.FloatField()
    total_quantity = serializers.IntegerField()


class CouponSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, value):
        try:
            coupon = Coupons.objects.get(
                code=value,
                valid_from__lte=now(),
                valid_until__gte=now(),
                is_active=True
            )
        except Coupons.DoesNotExist:
            raise serializers.ValidationError("This coupon is invalid or has expired.")
        return value




