# pagination.py (puede estar en el mismo archivo views.py o en un archivo separado)
from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Valor por defecto
    page_size_query_param = 'per_page'
    max_page_size = 100  # Máximo permitido por página

    def get_page_size(self, request):
        # Sobrescribe este método para depurar el tamaño de página solicitado
        page_size = super().get_page_size(request)
        print(f"Requested per_page: {request.query_params.get('per_page')}, Page size set to: {page_size}")
        return page_size
