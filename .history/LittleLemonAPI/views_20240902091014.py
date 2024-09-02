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

@api_view()
def menu_items(request):
    items = MenuItem.objects.all()

    # Filtrar por category_id si el parámetro de consulta 'category' está presente
    category_name = request.query_params.get('category')
    if category_name:
        category = Category.objects.filter(title__iexact=category_name).first()
        if category:
            items = items.filter(category_id=category.id)
        else:
            return Response({"error": "Category not found"}, status=404)

    # Filtrar por precio
    to_price = request.query_params.get('to_price')
    if to_price:
        try:
            to_price = float(to_price)
            items = items.filter(price__lte=to_price)
        except ValueError:
            return Response({"error": "Invalid price value"}, status=400)

    serialized_item = MenuItemSerializer(items, many=True)
    return Response(serialized_item.data)



'''@api_view()
def menu_items(request):
    items = MenuItem.objects.all()
    serialized_item = MenuItemSerializer(items, many=True)
    return Response(serialized_item.data)'''