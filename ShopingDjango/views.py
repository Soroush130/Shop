import itertools

from datetime import date, timedelta
from django.db.models import Sum, Avg, Max, Min

from django.shortcuts import render

from shop_contact.models import AboutUs
from shop_product.models import Product, Comment, Category, Slider


def mygrouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def home_page(request):
    # جدید ترین محصولات
    new_products = Product.objects.filter(active=True).order_by('-create_on')[:8]
    list_new_products = list(mygrouper(4, new_products))
    # ===============================================================================

    # ارزان ترین محصولات
    inexpensive = Product.objects.filter(price__lte=90000000, active=True)[:8]  # زیر 9 میلیون تومن
    list_inexpensive_products = list(mygrouper(4, inexpensive))
    # ================================================================================

    pr = Product.objects.filter(category__childern=None)

    """
      کد زیر برای فیلتر کردن محصولاتی که بیشترین رای را در داخل قسمت کامنت های است گرفته اند .
    """
    rates = Comment.objects.values('product__title', 'product__price', 'product__image', 'product_id', 'rate').annotate(
        rate_sum=Sum('rate')).order_by('-rate_sum')
    print(rates)
    list_rates_products = list(mygrouper(4, rates))
    # ==============================================================================================================

    """
    در قسمت زیر میتوانیم محصولات را در یک بازه زمانی خاص فیلتر کنیم که کد
    زیر برای فیلتر محصولات در یک هفته گذشته است . 
    """
    # enddate = date.today()
    # startdate = enddate - timedelta(days=6)
    # product = Product.objects.filter(create_on__range=[startdate, enddate])
    # =================================================================================

    """
     کد زیر برای فیلتر کردن محصولاتی است که بیشتر پسندیده شده اند .
    """
    favourite = Product.objects.filter(favourite__fa_user__count__gte=1).distinct()
    list_favourite_products = list(mygrouper(4, favourite))
    # ====================================================================

    slider = Slider.objects.filter(active=True)

    return render(request, 'home_page.html',
                  {'list_new_products': list_new_products,
                   'list_inexpensive_products': list_inexpensive_products, 'pr': pr,
                   'list_rates_products': list_rates_products,
                   'list_favourite_products': list_favourite_products,
                   'slider': slider, })


def header(request):
    return render(request, 'shared/Header.html', {})


def footer(request):
    about_us = AboutUs.objects.all().first()
    return render(request, 'shared/Footer.html', {'about_us': about_us})


def notfound_page(request):
    return render(request, '404.html', {})
