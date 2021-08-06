from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from django.shortcuts import render, redirect
from datetime import date, timedelta
from shop_cart.models import Order, ItemOrder, Cart
from shop_contact.models import ContactUs
from shop_product.models import Product
from shop_todo.models import ToDoForm, ToDo
from .forms import LoginUserForm, RegisterUserForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from shop_account.models import UserAccount, Profile
from django.utils import timezone


# Create your views here.

def header_profile(request):
    contact = ContactUs.objects.all()
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request, 'account/base_profile/header_profile.html', {'profile': profile, 'contact': contact, })


def footer_profile(request):
    return render(request, 'account/base_profile/footer_profile.html', {})


def login_page(request):
    url = request.META.get("HTTP_REFERER")
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        login_form = LoginUserForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                return redirect(url)
    else:
        login_form = LoginUserForm()

    context = {
        'login_form': login_form,
    }
    return render(request, 'account/login.html', context)


def log_out(request):
    logout(request)
    return redirect('/account/login')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        register_form = RegisterUserForm(request.POST)
        if register_form.is_valid():
            email = register_form.cleaned_data["email"]
            name = register_form.cleaned_data["name"]
            password = register_form.cleaned_data["password"]
            UserAccount.objects.create_user(email=email, name=name, password=password)
            return redirect('/account/login')
    else:
        register_form = RegisterUserForm()

    context = {
        'register_form': register_form,
    }
    return render(request, 'account/register.html', context)


@login_required(login_url='/login')
def user_profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    product = Product.objects.all()
    user = UserAccount.objects.all()

    todo = ToDo.objects.filter(user_id=request.user.id)
    paginator = Paginator(todo, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'product': product,
        'user': user,
        'page_obj': page_obj,
    }
    return render(request, 'account/profiel-user.html', context)


@login_required(login_url='/login')
def update_profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/account/profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'account/update.html', context)


@login_required(login_url='/login')
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "password change down", 'success')
            return redirect('/account/profile')
        else:
            messages.error(request, "password dose not exist", 'danger')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change-password.html', {'form': form})


@login_required(login_url='/login')
def favourite_list(request):
    favourite_product = request.user.fa_user.all()
    paginator = Paginator(favourite_product, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'account/favourite-list.html', context)


@login_required(login_url='/login')
def order_history(request):
    order = Order.objects.filter(user_id=request.user.id)
    item_order = ItemOrder.objects.filter(user_id=request.user.id)

    total = 0
    for o in item_order:
        total += (o.product.price * o.quantity)

    # taxation ==>> مالیات
    taxation = int((total * 9) / 100)

    final_price = 0
    for d in order:
        if d.discount:
            total_price = taxation + total
            discount_price = int((total_price * d.discount) / 100)
            final_price = total_price - discount_price
        else:
            final_price = taxation + total

    context = {
        'order': order,
        'item_order': item_order,
        'final_price': final_price,
    }
    return render(request, 'account/order-history.html', context)


@login_required(login_url='/login')
def product_list(request):
    product = Product.objects.all()
    paginator = Paginator(product, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'account/product-list.html', context)


@login_required(login_url='/login')
def search_list_product(request):
    query = request.GET.get('search')
    lookup = (
            Q(title__icontains=query) |
            Q(brand__title__icontains=query) |
            Q(category__parent__title__icontains=query)
    )

    filter_product = Product.objects.filter(lookup, active=True).distinct()
    paginator = Paginator(filter_product, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'account/product-list.html', context)


@login_required(login_url='/login')
def user_list(request):
    list_user = UserAccount.objects.all()
    paginator = Paginator(list_user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'account/user-list.html', context)


@login_required(login_url='/login')
def search_list_user(request):
    query = request.GET.get('U')
    lookup = (
            Q(email__icontains=query) |
            Q(name__iexact=query)
    )

    filter_user = UserAccount.objects.filter(lookup)
    paginator = Paginator(filter_user, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'account/user-list.html', context)


@login_required(login_url='/login')
def contact(request):
    contact = ContactUs.objects.all()
    return render(request, 'account/contact.html', {'contact': contact})
