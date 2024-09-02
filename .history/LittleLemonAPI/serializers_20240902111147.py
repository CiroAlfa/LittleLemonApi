from rest_framework import serializers
from .models import MenuItem
from decimal import Decimal
from .models import Category

class CategorySerializer(serializers.ModelSerializer):   
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']
        

class MenuItemSerializer(serializers.ModelSerializer):
    # Declaramos que el precio no puede ser menor a 2.0
    price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)
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