# accounts/session_manager.py
from cart.cart_operations import get_or_create_cart, transfer_cart_from_session_to_user

def handle_user_login(request, user):
    """Переносит корзину с сессии в корзину пользователя после входа."""
    # Перенос корзины
    transfer_success = transfer_cart_from_session_to_user(request, user)

    # Возвращаем результат
    return transfer_success
