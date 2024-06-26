from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms
from django.utils.text import slugify


# Create your views here.

def category(request, slug):
    # slug = slug.replace('-', ' ') # Replaced spaces with hyphen
    normalized_slug = slugify(slug)
    try:
        category = Category.objects.get(name=normalized_slug)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except Category.DoesNotExist:
        messages.warning(request, ("Category does not exist..."))
        return redirect(request, 'home')

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(req):
    return render(req, 'about.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Logged in successfully..."))
            return redirect('home')
        else:
            messages.warning(request, ("error, incorrect details..."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Logged out successfully..."))
    return redirect('login')


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Login User
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Account created successfully..."))
            return redirect('home')
        else:
            messages.success(request, ("Fill up the required details"))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})