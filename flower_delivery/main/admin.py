# admin.py

from django.contrib import admin
from .models import Flower
from .models import OrderStatus
from cart.models import Cart, CartItem

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Flower)


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'status')  # Показывать эти поля в списке заказов
    list_filter = ('status',)  # Фильтр по статусу заказа
    search_fields = ('user__username', 'status')  # Поиск по имени пользователя и статусу
    list_editable = ('status',)  # Возможность редактировать статус прямо в списке заказов