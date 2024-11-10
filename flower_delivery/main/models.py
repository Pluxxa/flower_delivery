# main/models.py
from django.db import models
from django.contrib.auth.models import User


class Flower(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default="Описание отсутствует")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(default="Описание отсутствует", upload_to='flowers/')

    def __str__(self):
        return self.name


class OrderStatus(models.Model):
    ORDER_STATUS_CHOICES = [
        ('received', 'Принят к работе'),
        ('in_progress', 'Находится в работе'),
        ('in_delivery', 'В доставке'),
        ('completed', 'Выполнен'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='received')

    def __str__(self):
        return f"Заказ от {self.order_date} — Статус: {self.get_status_display()}"
