from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .models import MenuItem
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
    # Obtener todos los elementos del menú
    items = MenuItem.objects.select_related('category').all()

    # Filtrar por categoría si el parámetro de consulta 'category' está presente
    category_name = request.query_params.get('category')
    if category_name:
        items = items.filter(category__title__iexact=category_name)
    
    # Filtrar por precio si el parámetro de consulta 'to_price' está presente
    to_price = request.query_params.get('to_price')
    if to_price:
        try:
            to_price = float(to_price)  # Convertir el parámetro a float
            items = items.filter(price__lte=to_price)
        except ValueError:
            # Si no se puede convertir a float, devolver una respuesta de error
            return Response({"error": "Invalid price value"}, status=400)
    
    # Serializar los elementos filtrados
    serialized_item = MenuItemSerializer(items, many=True)
    
    # Retornar la respuesta con los elementos filtrados
    return Response(serialized_item.data)


'''@api_view()
def menu_items(request):
    items = MenuItem.objects.all()
    serialized_item = MenuItemSerializer(items, many=True)
    return Response(serialized_item.data)'''