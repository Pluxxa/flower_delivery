# cart/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Пример маршрута для просмотра корзины
    path('', views.view_cart, name='view_cart'),
    # Пример маршрута для добавления товара в корзину
    path('add/<int:flower_id>/', views.add_to_cart, name='add_to_cart'),
    # Добавьте другие маршруты для корзины, если необходимо
]
