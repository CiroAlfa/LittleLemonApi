from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import Category, MenuItem
from .serializers import MenuItemSerializer
from rest_framework.decorators import api_view

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        # Obtenemos todos los elementos del menú
        queryset = MenuItem.objects.select_related('category').all()

        # Filtramos por categoría si se proporciona en la consulta
        category_name = self.request.query_params.get('category')
        if category_name:
            queryset = queryset.filter(category__title=category_name)

        # Filtramos por precio si se proporciona en la consulta
        max_price = self.request.query_params.get('to_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Filtramos por búsqueda en el nombre si se proporciona en la consulta
        search_term = self.request.query_params.get('search')
        if search_term:
            queryset = queryset.filter(title__icontains=search_term)

        return queryset

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def create_view(request):
    if request.method == 'GET':
        items = MenuItem.objects.all()
        category = request.query_params.get('category')
        if category:
            items = items.filter(category__title=category)
        search = request.query_params.get('search')
        if search:
            items = items.filter(title__startswith=search)
        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data)

    elif request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True) 
        serialized_item.save()
        


    serialized_item = MenuItemSerializer(items, many=True)
    return Response(serialized_item.data)



'''@api_view()
def menu_items(request):
    items = MenuItem.objects.all()
    serialized_item = MenuItemSerializer(items, many=True)
    return Response(serialized_item.data)'''