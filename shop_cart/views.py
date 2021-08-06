from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from shop_cart.models import CartForm, Cart, Order, CouponForm, OrderForm, ItemOrder, Coupon
from shop_product.models import Product

# Create your views here.


@login_required(login_url='/login')
def add_cart(request, id):
    url = request.META.get("HTTP_REFERER")
    data = Cart.objects.filter(user_id=request.user.id, product_id=id)
    if data:
        check = 'yes'
    else:
        check = 'no'
    if request.method == "POST":
        form = CartForm(request.POST)
        if form.is_valid():
            count = form.cleaned_data['quantity']
            if check == "yes":
                number = Cart.objects.get(product_id=id, user_id=request.user.id)
                number.quantity += count
                number.save()
            else:
                Cart.objects.create(product_id=id, user_id=request.user.id, quantity=count)

            return redirect(url)


@login_required(login_url='/login')
def cart_detail(request):
    carts = Cart.objects.filter(user_id=request.user.id)
    form_order = OrderForm()
    total = 0
    for cart in carts:
        total += (cart.product.price * cart.quantity)

    # مالیات
    taxation = int((total * 9) / 100)

    # مجموع کل سبد خرید
    total_carts = int(total + taxation)

    context = {
        'carts': carts,
        'total': total,
        'taxation': taxation,
        'total_carts': total_carts,
        'form_order': form_order,

    }
    return render(request, 'cart/cart-detaile.html', context)


@login_required(login_url='/login')
def remove_cart(request, id):
    url = request.META.get('HTTP_REFERER')
    Cart.objects.filter(id=id).delete()
    return redirect(url)


@login_required(login_url='/login')
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    form = CouponForm()
    cart = Cart.objects.filter(user_id=request.user.id)

    total = 0
    for c in cart:
        total += (c.product.price * c.quantity)

    # taxation ==>> مالیات
    taxation = int((total * 9) / 100)

    if order.discount:
        final_price = total + taxation
        final_price = int((final_price * order.discount) / 100)
    else:
        final_price = int(total + taxation)

    coupon = Coupon.objects.filter(active=True).first()

    context = {
        'order': order,
        'cart': cart,
        "form": form,
        'total': total,
        'taxation': taxation,
        'final_price': final_price,
        'coupon': coupon,
    }
    return render(request, 'cart/order.html', context)


@login_required(login_url='/login')
def order_create(request):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            order = Order.objects.create(user_id=request.user.id, email=data['email'], f_name=data['f_name'],
                                         l_name=data['l_name'], phone=data['phone'], address=data['address'],
                                         address_2=data['address_2']
                                         )
            cart = Cart.objects.filter(user_id=request.user.id)
            for c in cart:
                ItemOrder.objects.create(order_id=order.id, user_id=request.user.id, product_id=c.product_id,
                                         quantity=c.quantity)

            return redirect(f"/cart/order-detail/{order.id}")
        else:
            return HttpResponse('فرم را به درستی کامل کنید')


@require_POST
def coupon_order(request, order_id):
    form = CouponForm(request.POST)
    time = timezone.now()
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, start__lte=time, end__gte=time, active=True)
        except Coupon.DoesNotExist:
            messages.error(request, 'this code wrong', 'danger')
            return redirect(f"/cart/order-detail/{order_id}")
        order = Order.objects.get(id=order_id)
        order.discount = coupon.discount
        order.save()
    return redirect(f"/cart/order-detail/{order_id}")


@login_required(login_url='/login')
def add_single(request,id):
    url = request.META.get("HTTP_REFERER")
    cart = Cart.objects.get(id=id)
    product = Product.objects.get(id=cart.product.id)
    if product.count > cart.quantity:
        cart.quantity += 1
    cart.save()
    return redirect(url)


@login_required(login_url='/login')
def remove_single(request,id):
    url = request.META.get("HTTP_REFERER")
    cart = Cart.objects.get(id=id)
    if cart.quantity < 2:
        cart.delete()
    else:
        cart.quantity -= 1
        cart.save()
    return redirect(url)


