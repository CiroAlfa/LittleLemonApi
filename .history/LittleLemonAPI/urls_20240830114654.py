from django.urls import path
from .views import MenuItemView, SingleMenuItemView

urlpatterns = [
    path('menu-items/', MenuItemView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>/', SingleMenuItemView.as_view(), name='single-menu-item'),
]
