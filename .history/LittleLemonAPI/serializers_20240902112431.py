from rest_framework import serializers
from decimal import Decimal
from .models import MenuItem, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id']
        extra_kwargs = {
            'price': {'min_value': 2},
            'stock': {'min_value': 0}
        }

    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)
    
    def validate_price(self, value):
        if value < 2:
            raise serializers.ValidationError('Price should not be less than 2.0')
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('Stock cannot be negative')
        return value

    def validate(self, attrs):
        if attrs['price'] < 2:
            raise serializers.ValidationError('Price should not be less than 2.0')
        if attrs['inventory'] < 0:
            raise serializers.ValidationError('Stock cannot be negative')
        return super().validate(attrs)
