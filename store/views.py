from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from store.forms import ProductReviewForm
from .models import Product, Order, OrderItem, Cart, CartItem
import random
from django.db.models import Q

def home(request):
    all_products = list(Product.objects.all())
    featured_products = random.sample(all_products, min(5, len(all_products)))
    latest_products = sorted(all_products, key=lambda x: x.id, reverse=True)[:9]
    
    context = {
        'featured_products': featured_products,
        'latest_products': latest_products,
    }
    return render(request, 'home.html', context)

def product_list(request):
    products = Product.objects.all()
    query = request.GET.get('search')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    context = {
        'products': products,
        'query': query
    }
    return render(request, 'product_list.html', context)
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.products_review.all().order_by('-created_at')  # Retrieve reviews
    review_form = ProductReviewForm()  # Empty form for new reviews
    context = {
        'product': product,
        'reviews': reviews,
        'form': review_form,
    }
    return render(request, 'product_detail.html', context)

@login_required
def create_product_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        review_form = ProductReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product.id)
        else:
            # If form is invalid, show errors on product detail page
            reviews = product.products_review.all().order_by('-created_at')
            context = {
                'product': product,
                'reviews': reviews,
                'form': review_form,  # Form with validation errors
            }
            return render(request, 'product_detail.html', context)
    return redirect('product_detail', product_id=product.id)
        

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    if request.method == 'POST':
        # Process the order
        order = Order.objects.create(user=request.user, total=0)
        total = 0
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            total += item.product.price * item.quantity
        order.total = total
        order.save()
        cart.items.all().delete()
        return redirect('my_orders')
    return render(request, 'checkout.html', {'cart': cart})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})

@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('profile')
    return render(request, 'profile.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')


@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = cart.total_price()
    return render(request, 'cart.html', {'cart': cart, 'cart_items': cart_items, 'total_price': total_price})


def about_us(request):
    return render(request, 'aboutus.html')

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you would typically send an email or save the contact form data
        # For now, we'll just add a success message
        messages.success(request, 'Thank you for your message. We will get back to you soon!')
        return redirect('contact_us')
    
    return render(request, 'contact_us.html')