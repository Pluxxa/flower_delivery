from django.shortcuts import render, get_object_or_404, redirect
from .models import Flower
from django.contrib.auth.models import User  # Если используем встроенную модель User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem


def home(request):
    flowers = Flower.objects.all()
    return render(request, 'main/home.html', {'flowers': flowers})


# Представление для отображения каталога цветов
def flower_list(request):
    flowers = Flower.objects.all()  # Получаем все цветы из базы данных
    flowers_dict = {flower.id: flower for flower in flowers}  # Создаем словарь с ключами — ID цветов
    return render(request, 'main/flower_list.html', {'flowers': flowers, 'flowers_dict': flowers_dict})


# Представление для отображения деталей конкретного цветка
def flower_detail(request, pk):
    flower = get_object_or_404(Flower, pk=pk)  # Получаем цветок по его первичному ключу
    return render(request, 'main/flower_detail.html', {'flower': flower})


# Представление для добавления цветка в корзину
# Пример в представлении
def get_cart(request):
    """ Получаем или создаем корзину для пользователя/сессии. """
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def add_to_cart(request, flower_id):
    """ Добавляем товар в корзину. """
    flower = Flower.objects.get(id=flower_id)
    cart = get_cart(request)

    # Проверяем, есть ли уже товар в корзине
    cart_item, created = CartItem.objects.get_or_create(cart=cart, flower=flower)

    # Если товар уже есть, увеличиваем количество
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


def cart(request):
    """ Отображаем корзину пользователя. """
    cart = get_cart(request)

    return render(request, 'main/cart.html', {'cart': cart})


def contacts(request):
    return render(request, 'main/contacts.html')  # Создайте шаблон для страницы контактов


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
            messages.success(request, 'Регистрация прошла успешно')
            return redirect('home')  # Замените на нужный URL после регистрации

    return render(request, 'main/register.html')


@login_required
def account(request):
    return render(request, 'main/account.html')