from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from shop_blog.models import Blog, RateBlogForm, RateBlog, CommentForm, Comment
from shop_product.models import Category, Brand


def blog_list(request):
    list_blog = Blog.objects.all()
    paginator = Paginator(list_blog, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    brands = Brand.objects.all()
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'blog/blog.html', context)


def blog_detail(request, id):
    try:
        blog = Blog.objects.get(id=id)
    except:
        return redirect('/404')

    # prev page blog
    prev = blog.id - 1
    if prev == 0:
        prev = 1

    # next page blog
    next = blog.id + 1
    list_blog = Blog.objects.all()
    if next > list_blog.count():
        next = blog.id

    categories = Category.objects.all()
    brands = Brand.objects.all()
    form = RateBlogForm()
    comment_form = CommentForm()
    comment = Comment.objects.all().order_by('-id')


    context = {
        'blog': blog,
        'categories': categories,
        'brands': brands,
        'prev': prev,
        'next': next,
        'form': form,
        'comment_form': comment_form,
        'comment': comment,
    }
    return render(request, 'blog/blog-detail.html', context)


def rate_blog(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        form = RateBlogForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['rate']
            rate = RateBlog.objects.create(user_id=request.user.id, blog_id=id, rate=data)
            rate.save()
            return redirect(url)


@login_required(login_url='/login')
def comment_product(request, id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            Comment.objects.create(comment=data['comment'], user_id=request.user.id, blog_id=id, is_reply=False)
            return redirect(url)


@login_required(login_url='/login')
def reply_comment_product(request, blog_id, comment_id):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            data = comment_form.cleaned_data
            Comment.objects.create(comment=data['comment'], user_id=request.user.id, blog_id=blog_id,
                                   reply_id=comment_id, is_reply=True)
            return redirect(url)
