from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework.decorators import api_view
from rest_framework import status

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


@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()

        # Filtrar por categoría
        category_name = request.query_params.get('category')
        if category_name:
            items = items.filter(category__title__iexact=category_name)

        # Filtrar por precio máximo
        max_price = request.query_params.get('to_price')
        if max_price:
            items = items.filter(price__lte=max_price)

        # Filtrar por búsqueda en el nombre
        search = request.query_params.get('search')
        if search:
            items = items.filter(title__icontains=search)

        # Ordenar los resultados
        ordering = request.query_params.get('ordering')
        if ordering:
            ordering_fields = ordering.split(',')
            items = items.order_by(*ordering_fields)

        serialized_items = MenuItemSerializer(items, many=True)
        return Response(serialized_items.data)

    elif request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)
