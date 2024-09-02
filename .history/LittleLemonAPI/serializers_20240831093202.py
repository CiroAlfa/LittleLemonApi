from rest_framework import serializers
from .models import MenuItem

@api_view()
def menu_items(request):
    items = MenuItem.objects.all()
    return Response(items.values())
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'inventory']
