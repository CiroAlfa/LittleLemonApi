from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import EmptyPage
from rest_framework.exceptions import NotFound
# views.py
from .pagination import CustomPageNumberPagination

from rest_framework.pagination import PageNumberPagination

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        queryset = MenuItem.objects.select_related('category').all()

        # Filtrar por categoría
        category_name = self.request.query_params.get('category')
        if category_name:
            queryset = queryset.filter(category__title__iexact=category_name)

        # Filtrar por precio máximo
        max_price = self.request.query_params.get('to_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Filtrar por búsqueda en el nombre
        search_term = self.request.query_params.get('search')
        if search_term:
            queryset = queryset.filter(title__icontains=search_term)

        # Ordenar los resultados
        ordering = self.request.query_params.get('ordering')
        if ordering:
            ordering_fields = ordering.split(',')
            queryset = queryset.order_by(*ordering_fields)

        return queryset


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer






  # Asegúrate de importar correctamente

from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'per_page'
    max_page_size = 100  # Máximo permitido por página

class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    pagination_class = CustomPageNumberPagination  # Añadir esta línea

    def get_queryset(self):
        queryset = MenuItem.objects.select_related('category').all()

        # Filtrar por categoría
        category_name = self.request.query_params.get('category')
        if category_name:
            queryset = queryset.filter(category__title__iexact=category_name)

        # Filtrar por precio máximo
        max_price = self.request.query_params.get('to_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Filtrar por búsqueda en el nombre
        search_term = self.request.query_params.get('search')
        if search_term:
            queryset = queryset.filter(title__icontains=search_term)

        # Ordenar los resultados
        ordering = self.request.query_params.get('ordering')
        if ordering:
            ordering_fields = ordering.split(',')
            queryset = queryset.order_by(*ordering_fields)

        return queryset


    
# En tu archivo views.py

from django.http import JsonResponse
from .custom_queries import get_menu_items_with_limit

def menu_items_limited(request):
    # Obtenemos el parámetro 'limit' de la URL, con un valor predeterminado de 10
    limit = request.GET.get('limit', 10)
    try:
        # Convertimos el límite a un entero
        limit = int(limit)
    except ValueError:
        # Si el límite no es un número válido, devolvemos un error
        return JsonResponse({"error": "Invalid limit parameter"}, status=400)
    
    # Obtenemos los elementos del menú utilizando nuestra función personalizada
    items = get_menu_items_with_limit(limit)
    # Devolvemos los elementos como una respuesta JSON
    return JsonResponse({"items": items})


# views.py

@api_view(['GET'])
def test_pagination(request):
    items = MenuItem.objects.all()
    paginator = CustomPageNumberPagination()
    paginated_items = paginator.paginate_queryset(items, request)
    serializer = MenuItemSerializer(paginated_items, many=True)
    return paginator.get_paginated_response(serializer.data)
