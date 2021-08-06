import itertools
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
# from django.views.generic import ListView
from shop_cart.models import CartForm
from shop_product.forms import CommentForm
from shop_product.models import Product, Gallery, Category, Brand, Comment, Chart


def product_list(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.filter(active=True)
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'product/product-list.html', context)


# class product_list(ListView):
#     queryset = Product.objects.filter(active=True)
#     template_name = 'product/product-list.html'
#     paginate_by = 1
#
#     def get_context_data(self,*args, **kwargs):
#         context = super().get_context_data(*args, **kwargs)
#         context['categories'] = Category.objects.all()
#         context['brands'] = Brand.objects.all()
#         return context


def mygrouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def mygrouper_segg(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except:
        return redirect('/404')

    # برای تغییرات قیمت
    update_price = Chart.objects.filter(product_id=product)

    gallery_product = Gallery.objects.filter(product_id=product)
    list_gallery = list(mygrouper(3, gallery_product))
    categories = Category.objects.all()
    brands = Brand.objects.all()
    comment_form = CommentForm()
    comments = Comment.objects.filter(product_id=product).order_by('-id')
    is_favourite = False
    if product.favourite.filter(id=request.user.id).exists():
        is_favourite = True

    # محصولات پیشنهادی
    suggested_product = Product.objects.get_queryset().filter(category__parent=product.category.parent).distinct()
    list_suggested_product = list(mygrouper_segg(3, suggested_product))
    # ===========================================================================================

    """
        قطعه کد زیر برای اینکه میاد محاسبه میکنه یک پست ایا جدیده یا یک پست قدیمی (در بازی زمانی 5 ساعته).
    """
    now = timezone.now()
    is_new_product = True
    if now.hour > product.create_on.hour + 5:
        # print('old')
        is_new_product = False
    elif product.create_on.hour <= now.hour <= product.create_on.hour + 5:
        # print('new')
        is_new_product = True
    # ============================================================================

    cart_form = CartForm()


    context = {
        'product': product,
        'list_gallery': list_gallery,
        'categories': categories,
        'brands': brands,
        'comment_form': comment_form,
        'comments': comments,
        'is_favourite': is_favourite,
        'list_suggested_product': list_suggested_product,
        'is_new_product': is_new_product,
        'cart_form': cart_form,
        'update_price': update_price,
    }
    return render(request, 'product/product-detail.html', context)


def category_product(request, slug):
    product_category = Product.objects.filter(category__slug=slug)

    paginator = Paginator(product_category, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    brands = Brand.objects.all()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'product/product-list.html', context)


def brand_category_product(request, slug):
    brand_products = Product.objects.filter(brand__slug=slug)

    paginator = Paginator(brand_products, 12)  # Show 12 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    brands = Brand.objects.all()
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
        'brand_products': brand_products,
    }
    return render(request, 'product/product-list.html', context)


def filter_price_product(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    product = Product.objects.filter(price__gte=min_price, price__lte=max_price)
    paginator = Paginator(product, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    brands = Brand.objects.all()
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'product/product-list.html', context)


# @login_required(login_url='/login')
def product_comment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.cleaned_data['comment']
            rate = comment_form.cleaned_data['rate']
            Comment.objects.create(comment=comment, rate=rate, user_id=request.user.id, product_id=id)
            return redirect(url)
        else:
            return HttpResponse('لطفا فرم را کامل پر کنید')
    else:
        comment_form = CommentForm()


@login_required(login_url='/login')
def favourite_product(request, id):
    url = request.META.get('HTTP_REFERER')
    try:
        product = Product.objects.get(id=id)
    except:
        return redirect('/404')

    is_favourite = False
    if product.favourite.filter(id=request.user.id).exists():
        product.favourite.remove(request.user)
        is_favourite = False
    else:
        product.favourite.add(request.user)
        is_favourite = True
    return redirect(url)


# برای باکس سرچ در قسمت هدر سایت
def search_header(request):
    query = request.GET.get('q')
    lookup = (
            Q(title__icontains=query) |
            Q(brand__title__icontains=query) |
            Q(category__parent__title__icontains=query)
    )

    filter_product = Product.objects.filter(lookup, active=True).distinct()
    paginator = Paginator(filter_product, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    brands = Brand.objects.all()
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'product/product-list.html', context)
