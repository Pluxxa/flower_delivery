from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .session_manager import handle_user_login


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            transfer_success = handle_user_login(request, user)
            if transfer_success:
                print("Корзина успешно перенесена.")
            return redirect("home")
        else:
            print("Ошибка входа")
    return render(request, "accounts/login.html")
