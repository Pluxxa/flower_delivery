# cart/cart_operations.py
from .models import Cart, CartItem

def transfer_cart_from_session_to_user(request, user):
    """ Переносит корзину с сессии в корзину пользователя. """
    session_key = request.session.session_key

    # Проверяем, существует ли корзина сессии
    session_cart = Cart.objects.filter(session_key=session_key).first()

    if session_cart and session_cart.user is None:
        # Создаем корзину для пользователя, если она еще не существует
        user_cart, _ = Cart.objects.get_or_create(user=user)

        # Переносим товары из сессионной корзины в пользовательскую корзину
        transfer_cart_items(session_cart, user_cart)

        return True  # Успешный перенос
    return False  # Корзина сессии не найдена или уже была перенесена

def get_or_create_cart(request, user=None):
    """
    Возвращает корзину пользователя (если авторизован) или корзину для сессии (если не авторизован).
    """
    if user and user.is_authenticated:
        # Корзина для авторизованного пользователя
        return Cart.objects.get_or_create(user=user)
    else:
        # Для неавторизованного пользователя корзина привязывается к session_key
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
            session_key = request.session.session_key
        return Cart.objects.get_or_create(session_key=session_key)

def transfer_cart_items(session_cart, user_cart):
    """
    Переносит товары из корзины сессии в корзину пользователя.
    """
    for item in session_cart.items.all():
        CartItem.objects.create(cart=user_cart, flower=item.flower, quantity=item.quantity)
    session_cart.delete()

def add_item_to_cart(cart, flower, quantity=1):
    """
    Добавляет товар в корзину. Если товар уже есть, увеличивает количество.
    """
    cart_item, created = CartItem.objects.get_or_create(cart=cart, flower=flower)
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
