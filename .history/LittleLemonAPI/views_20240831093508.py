from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer

from rest_framework.decorators import api_view

@api_view()
def menu_items(request):
    items = MenuItem.objects.all()
    return Response(items.values())

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
