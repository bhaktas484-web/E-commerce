
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login

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
    product_id = str(product_id)

    # Add item to cart
    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    return redirect('cart')


# Remove from cart view
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart')


# Cart view
from .models import Product

from .models import Product

def cart(request):
    session_cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in session_cart.items():

        if not product_id.isdigit():  
            # SKIP invalid or empty keys
            continue  

        try:
            product = Product.objects.get(id=int(product_id))
        except Product.DoesNotExist:
            continue

        item_total = product.price * quantity
        total_price += item_total

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': item_total
        })

    discount = round(total_price * 0.05, 2)
    grand_total = total_price - discount

    return render(request, "home/cart.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "discount": discount,
        "grand_total": grand_total,
    })

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

    total_price = sum(product.price * cart[str(product.id)] for product in products)

    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')


        # Clear cart after placing order
        request.session['cart'] = {}

        # Redirect to success page
        return redirect('checkout_success')

    return render(request, "home/checkout.html", {
        "products": products,
        "cart_items": cart,
        "total_price": total_price,
    })
def checkout_success(request):
    return render(request, "home/checkout_success.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)  # Auto login
        return redirect("home")  # Redirect to home page

    # IMPORTANT: this return must NOT be on same line as "if"
    return render(request, "home/register.html")

#searching
def search(request):
    query = request.GET.get("query", "")
    results = Product.objects.filter(name__icontains=query)
    return render(request, "home/search.html", {"results": results, "query": query})

#contacts view
from django.shortcuts import render, redirect
from .models import ContactMessage
from django.contrib import messages

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        msg = request.POST.get("message")

        ContactMessage.objects.create(
            name=name,
            email=email,
            message=msg
        )


        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")

    return render(request, "home/contact.html")
