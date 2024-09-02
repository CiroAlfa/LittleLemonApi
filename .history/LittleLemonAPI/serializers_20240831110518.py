from rest_framework import serializers
from .models import MenuItem
from decimal import Decimal
from .models import Category

class MenuItemSerializer(serializers.ModelSerializer):   
    class Meta:
        model = MenuItem
        fields = ['id', 'slug', 'title']
        

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name = 'calculate_tax')
    category = CategotySerializer()
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category']
        
    def calculate_tax(self, product:MenuItem):
        return (product.price * Decimal ('1.1'),2)
    
    
    
    
    
#antigua forma mas complicada
'''class MenuItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.IntegerField()'''