from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import CustomUser
# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect("dashboard:main")
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request,email=email,password=password)

        if user is not None:
            auth_login(request,user)
            success_message = "Anda telah login"
            messages.success(request, success_message)
            return redirect("dashboard:main")
        else:
            warning_message = "Kredential salah coba cek email dan password"
            messages.warning(request,warning_message)
            return render(request,'login.html')
    return render(request,'login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard:main")
    if request.method == "POST":
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = CustomUser(nama=nama,email=email,password=password,role="User")
        user.save()
        return redirect('authentication:login-form')
    return render(request,'register.html')

def logout_view(request):
    logout(request)
    return redirect('authentication:login-form')