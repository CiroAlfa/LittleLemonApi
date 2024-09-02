from django.urls import path
from .views import MenuItemView, SingleMenuItemView, menu_items_limited

urlpatterns = [
    path('menu-items/', MenuItemView.as_view(), name='menu-items'),
    path('menu-items/<int:pk>/', SingleMenuItemView.as_view(), name='single-menu-item'),
    path('menu-items-limited/', menu_items_limited, name='menu-items-limited'),

]
