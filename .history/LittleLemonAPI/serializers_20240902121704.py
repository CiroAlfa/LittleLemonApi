from rest_framework import serializers
from decimal import Decimal
from .models import MenuItem, Category
import bleach 
from rest_framework import serializers
from .models import MenuItem, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

# En tu archivo serializers.py

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id']

    def validate_title(self, value):
        # Saneamos el título usando bleach para eliminar cualquier HTML malicioso
        return bleach.clean(value)

    def validate(self, attrs):
        # Saneamos el título nuevamente en el método validate por si acaso
        attrs['title'] = bleach.clean(attrs['title'])
        
        # Validaciones adicionales
        if attrs['price'] < 2:
            raise serializers.ValidationError('Price should not be less than 2.0')
        if attrs['inventory'] < 0:
            raise serializers.ValidationError('Stock cannot be negative')
        return super().validate(attrs)

    def calculate_tax(self, product: MenuItem):
        # Cálculo del precio después de impuestos
        return product.price * Decimal(1.1)