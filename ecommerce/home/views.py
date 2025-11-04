
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Home page view
def home(request):
    products = Product.objects.all()
    return render(request, 'home/home.html', {'products': products})

# Product details view
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'home/product_detail.html', {'product': product})

# Cart view
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product

def cart(request):
    cart = request.session.get('cart', {})  # Get cart dictionary from session
    products = Product.objects.filter(id__in=cart.keys())

    total_price = 0
    for product in products:
        total_price += product.price * cart[str(product.id)]  # Calculate total

    return render(request, 'home/cart.html', {
        'products': products,
        'cart_items': cart,
        'total_price': total_price
    })


# Add to cart view
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')
# Remove from cart view
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart') 

# Increase quantity
def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1
    request.session['cart'] = cart
    return redirect('cart')

# Decrease quantity
def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1
        else:
            # remove if quantity becomes 0
            del cart[str(product_id)]
    request.session['cart'] = cart
    return redirect('cart')


def checkout(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    total_price = 0
    for product in products:
        total_price += product.price * cart[str(product.id)]

    return render(request, 'home/checkout.html', {
        'products': products,
        'cart_items': cart,
        'total_price': total_price
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # After registration, go to login page
    else:
        form = UserCreationForm()
    return render(request, 'home/register.html', {'form': form})


