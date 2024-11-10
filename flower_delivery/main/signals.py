# main/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from cart.models import Cart

@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    """ Функция для переноса товаров из корзины сессии в корзину пользователя после логина. """
    # Импорт внутри функции, чтобы избежать циклической зависимости
    from cart.cart_operations import transfer_cart_from_session_to_user

    # Проверяем, есть ли session_key в сессии
    if request.session.session_key:
        session_key = request.session.session_key

        # Ищем корзину сессии по session_key
        cart = Cart.objects.filter(session_key=session_key).first()

        if cart:
            # Если корзина существует и она не привязана к пользователю, связываем с пользователем
            if cart.user is None:
                cart.user = user
                cart.session_key = ""  # Очищаем session_key после связывания с пользователем
                cart.save()
            elif cart.user != user:
                pass
