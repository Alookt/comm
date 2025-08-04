# store/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem, Order, OrderItem
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm,RegisterForm
from django.contrib.auth import authenticate, login
from rest_framework.generics import ListAPIView
from .serializers import ProductSerializer
from django.shortcuts import render
from .services.rainforest import search_amazon_products




def amazon_search(request):
    results = []
    search_term = request.GET.get('q')
    if search_term:
        data = search_amazon_products(search_term)
        if data and "search_results" in data:
            results = data["search_results"]

    return render(request, 'products/amazon_results.html', {"results": results, "search_term": search_term})




class ProductListAPI(ListAPIView):
    queryset = Product.objects.all().order_by('id') 
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # This returns the saved User instance
            # Authenticate user before login to set backend info
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')
            else:
                form.add_error(None, 'Authentication failed after registration.')
    else:
        form = RegisterForm()
    return render(request, 'opp/register.html', {'form': form})




def product_list(request):
    products = Product.objects.all()
    return render(request, 'opp/product_list.html', {'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'opp/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)  # or however you get cart
    total = 0
    for item in cart_items:
        item.total_price = item.product.price * item.quantity  # add attribute for template
        total += item.total_price
    context = {
        'cart_items': cart_items,
        'total': total,
    }
    return render(request, 'opp/cart.html', context)


@login_required
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, product_id=product_id, user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, complete=True)
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
        cart_items.delete()  # Clear cart after order
        return redirect('order_confirmation', order_id=order.id)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'opp/checkout.html', {'cart_items': cart_items, 'total': total})

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'opp/order_confirmation.html', {'order': order})


@login_required
def profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'opp/profile.html', {'form': form})