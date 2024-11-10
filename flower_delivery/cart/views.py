# cart/views.py
from django.shortcuts import render
from .cart_operations import get_or_create_cart
from django.shortcuts import redirect, get_object_or_404
from main.models import Flower
from django.http import HttpResponseBadRequest
# views.py
import logging

logger = logging.getLogger(__name__)

def view_cart(request):
    cart, _ = get_or_create_cart(request, request.user)
    cart_items = cart.items.all()

    logger.debug(f"Cart items: {cart_items}")  # Логируем все элементы корзины

    return render(request, 'cart/view_cart.html', {'cart_items': cart_items})

def add_to_cart(request, flower_id, quantity=1):
    cart, created = get_or_create_cart(request, request.user)
    flower = get_object_or_404(Flower, id=flower_id)

    logger.debug(f"Adding flower {flower.name} with quantity {quantity} to cart")

    if quantity <= 0:
        return HttpResponseBadRequest("Количество товара должно быть больше нуля.")

    cart_item, created = cart.items.get_or_create(flower=flower)
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    logger.debug(f"Cart after adding item: {cart.items.all()}")

    return redirect('cart:view_cart')
