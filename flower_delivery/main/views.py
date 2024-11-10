from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Flower
from cart.cart_operations import get_or_create_cart, add_item_to_cart, transfer_cart_from_session_to_user

def home(request):
    flowers = Flower.objects.all()
    return render(request, 'main/home.html', {'flowers': flowers})

def flower_list(request):
    flowers = Flower.objects.all()
    flowers_dict = {flower.id: flower for flower in flowers}
    return render(request, 'main/flower_list.html', {'flowers': flowers, 'flowers_dict': flowers_dict})

def flower_detail(request, pk):
    flower = get_object_or_404(Flower, pk=pk)
    return render(request, 'main/flower_detail.html', {'flower': flower})

def get_cart(request):
    cart, _ = get_or_create_cart(request)
    return cart

def add_to_cart(request, flower_id):
    flower = Flower.objects.get(id=flower_id)
    cart = get_cart(request)
    add_item_to_cart(cart, flower)
    return redirect('cart')

def cart(request):
    cart = get_cart(request)
    return render(request, 'main/cart.html', {'cart': cart})

def contacts(request):
    return render(request, 'main/contacts.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Проверка, существует ли уже такой пользователь
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return redirect('register')

        # Создание нового пользователя
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Автоматическая авторизация после регистрации
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Переносим корзину из сессии в корзину пользователя
            if transfer_cart_from_session_to_user(request, user):
                messages.success(request, 'Ваши товары были перенесены в вашу корзину.')
            else:
                messages.info(request, 'Ваша корзина была пуста.')

            messages.success(request, 'Регистрация прошла успешно')
            return redirect('home')

    return render(request, 'main/register.html')

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('home')

@login_required
def account(request):
    user_cart = get_cart(request)
    user_cart_items = user_cart.items.all() if user_cart else []

    return render(request, 'main/account.html', {
        'user_cart': user_cart,
        'user_cart_items': user_cart_items,
    })
