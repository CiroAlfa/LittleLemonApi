from rest_framework import serializers
from decimal import Decimal
from .models import MenuItem, Category

# Serializador para la categoría
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

# Serializador para el ítem del menú
class MenuItemSerializer(serializers.ModelSerializer):
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id']
    
#antigua forma mas complicada
'''class MenuItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.IntegerField()'''