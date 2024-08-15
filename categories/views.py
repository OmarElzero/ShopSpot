from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import Product, CartItem, Cart, Category, Order, OrderItem
from profiles.forms import ProductSearchForm, RegistrationForm

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import reverse




# Create your views here.


def cart_page(request):
    current_user = request.user
    quantity = request.GET.get('quantity', None)
    try:
        crt = Cart.objects.get(user=current_user)
        cart_items = crt.items.all()
        total = 0
        for c in cart_items:
            total = total + c.total()
        return render(request, 'categories/cart.html', {'cart_items': cart_items, 'total': total, 'quantity': quantity})
    except:
        return render(request, 'categories/cart.html')


@login_required
def add_to_cart(request, product_id):
    current_user = request.user
    item = get_object_or_404(Product, id=product_id)
    qty = 1

    if not request.user.is_authenticated:
        return redirect('login_page')

    try:
        user_cart = Cart.objects.get(user=current_user)
        cart_item = user_cart.items.filter(item=item).first()

        if cart_item:
            new_total_quantity = cart_item.quantity + qty
            # Check if the new total quantity exceeds the available stock
            if new_total_quantity > item.quantity:
                messages.error(request, "Sorry, It seems like requested quantity is more than available stock!")
                return redirect('shop')

            cart_item.quantity = new_total_quantity
            cart_item.price = item.price * new_total_quantity
            cart_item.save()
        else:
            new_cart_item = CartItem(item=item, quantity=qty, price=item.price)
            new_cart_item.save()
            user_cart.items.add(new_cart_item)
            cart_item = new_cart_item

        return redirect(reverse('cart') + f'?quantity={cart_item.quantity}')

    except Cart.DoesNotExist:
        user_cart = Cart(user=current_user)
        user_cart.save()
        new_cart_item = CartItem(item=item, quantity=qty, price=item.price)
        new_cart_item.save()
        user_cart.items.add(new_cart_item)
        return redirect(reverse('cart') + f'?quantity={qty}')


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart = Cart.objects.get(user=request.user)
    if cart_item in cart.items.all():
        cart.items.remove(cart_item)
    return redirect('cart')


@login_required
def clear_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart.items.clear()
    return redirect('cart')


def order_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # Create a new order for the user
        order = Order.objects.create(user=request.user, total_price=product.price)

        # Create an order item for the product
        OrderItem.objects.create(order=order, product=product, quantity=1, item_price=product.price)

        # Decrease the product quantity by 1
        product.quantity -= 1
        product.save()

        return redirect('view_ordered_items')  # Redirect to the orders page

    context = {'product': product, 'default_quantity': 1}
    return render(request, 'categories/order_now.html', context)


@login_required
def cart_order_now(request):
    cart_items = CartItem.objects.filter(cart=request.user.cart)
    total_price = sum(item.total() for item in cart_items)

    # Check if any cart item quantity is out of stock
    for cart_item in cart_items:
        if cart_item.quantity > cart_item.item.quantity:
            # messages.warning(request, f"Quantity of {cart_item.item.name} reduced to available stock.")
            cart_item.quantity = cart_item.item.quantity
            cart_item.save()

    # Filter out cart items with a quantity of zero
    cart_items = cart_items.exclude(quantity=0)

    if request.method == 'POST':
        # Create the order and order items for the cart items
        order = Order.objects.create(user=request.user, total_price=total_price)

        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.item,
                quantity=cart_item.quantity,
                item_price=cart_item.item.price * cart_item.quantity
            )

            # Decrease the product quantity by the ordered quantity
            cart_item.item.quantity -= cart_item.quantity
            cart_item.item.save()

        # Mark cart items as ordered
        cart_items.update(is_ordered=True)

        # Clear the user's cart by deleting cart items
        cart_items.delete()

        return redirect('view_ordered_items')  # Redirect to the orders page

    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'categories/cart_order_now.html', context)


def view_ordered_items(request):
    orders = Order.objects.filter(user=request.user)
    order_items = OrderItem.objects.filter(order__in=orders)
    return render(request, 'categories/orders.html', {'order_items': order_items})


def filter_by_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    products = Product.objects.filter(category=category, quantity__gt=0)  # Filter by category and quantity > 0
    categories = Category.objects.all()
    return render(request, 'categories/product_list_by_category.html', {'products': products, 'categories': categories})


def search_products(request):
    form = ProductSearchForm()
    query = None
    results = []

    if 'search_query' in request.GET:
        form = ProductSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['search_query']
            results = Product.objects.filter(name__icontains=query, quantity__gt=0)  # Filter by name and quantity > 0

    return render(request, 'categories/search_result.html', {'form': form, 'query': query, 'results': results})

def product_details(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'categories/product_des.html', context)