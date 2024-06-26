from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm

# Create your views here.
def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "GET":
        return render(request, "login.html", {"form": UserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                # Registro de usuario
                user = User.objects.create_user(
                    username=request.POST["username"],
                    email=request.POST["email"],
                    password=request.POST["password1"],
                )
                user.save()
                print (user.password)
                # login(request, user)
                return redirect("signin")
            except IntegrityError:
                return render(
                    request,
                    "login.html",
                    {"form": UserCreationForm, "error": "El usuario ingresado ya existe"},
                )
        return render(
            request,
            "login.html",
            {"form": UserCreationForm, 
            "error": "Las contraseñas no coinciden"},
        )

def dashboard(request):
    return render(request, "dashboard.html")

def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {"form": TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("dashboard")
        except ValueError:
            return render(
                request,
                "create_task.html",
                {"form": TaskForm, "error": "Por favor ingrese datos válidos"},
            )

def signout(request):
    logout(request)
    return redirect("home")

def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        ) 
        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Usuario o contraseña incorrectos",
                },
            )
        else:
            login(request, user)
            return redirect("dashboard")
        
    if request.method == "GET":
        return render(request, "recover.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            key=request.POST["recoverpassword"],
        )
        if user is None:
            return render(
                request,
                "recover.html",
                {
                    "form": AuthenticationForm,
                    "error": "Recovery password incorrect",
                },
            )
        else:
            login(request, user)
            return redirect("dashboard")

def about_us(request):
    return render(request, "about_us.html")
