from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .models import Order

from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Product, Cart
from django.contrib.auth.models import User

def home(request):

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    cart_count = 0
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()

    return render(request,'home.html',{
        'products':products,
        'cart_count':cart_count
    })

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('home')

def landing(request):
    return render(request,'landing.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')

def signup_view(request):
    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'signup.html')

def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.product.price * item.quantity

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def remove_from_cart(request, cart_id):
    item = Cart.objects.get(id=cart_id)
    item.delete()
    return redirect('cart')

def logout_view(request):
    logout(request)
    return redirect('landing')

def product_detail(request, product_id):

    product = Product.objects.get(id=product_id)

    return render(request,'product_detail.html',{
        'product':product
    })


@login_required
def profile(request):

    cart_count = Cart.objects.filter(user=request.user).count()

    return render(request,'profile.html',{
        'user':request.user,
        'cart_count':cart_count
        
    })


@login_required
def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)

    if request.method == "POST":

        address = request.POST.get("address")
        phone = request.POST.get("phone")

        order = Order.objects.create(
            user=request.user,
            address=address,
            phone=phone
        )

        cart_items.delete()

        return redirect('order_confirmation', order_id=order.id)

    return render(request, "checkout.html")

@login_required
def order_confirmation(request, order_id):

    order = Order.objects.get(id=order_id)

    return render(request, "order_confirmation.html", {
        "order": order
    })

@login_required
def my_orders(request):

    orders = Order.objects.filter(user=request.user)

    return render(request, "orders.html", {
        "orders": orders
    })


def search(request):
    query = request.GET.get('query')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'home.html', {'products': products})