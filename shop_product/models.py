from shop_account.models import UserAccount
from django.db import models
from django.db.models.signals import post_save


# Create your models here.

class Brand(models.Model):
    title = models.CharField(max_length=80)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='childern', default=None, null=True,
                               blank=True)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=125)
    price = models.PositiveIntegerField()
    """
        برای اینکه بتونیم تغییرات قیمت رو در داخل مدل Chart ذخییره کنیم  
         باید فیلد change را برابر False بگیریم
    """
    change = models.BooleanField(default=True)

    count = models.PositiveIntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_product')
    # rate = models.PositiveIntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_product', default=None)
    image = models.ImageField(upload_to="product", null=True, blank=True)
    # موجودی
    inventory = models.BooleanField(default=True)
    discount = models.IntegerField(null=True, blank=True)
    body = models.TextField(max_length=300, null=True, blank=True)
    active = models.BooleanField(default=True)
    favourite = models.ManyToManyField(UserAccount, blank=True, related_name='fa_user')
    create_on = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='gallery-image')

    def __str__(self):
        return self.title


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='co_pr')
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    comment = models.TextField()
    rate = models.PositiveIntegerField(default=1)
    create_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title


# مدل تقییرات قیمت
class Chart(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.PositiveIntegerField(default=0)
    update = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='pr_update', null=True, blank=True)

    def __str__(self):
        return self.name


def product_post_save(sender, instance, created, *args, **kwargs):
    data = instance
    if data.change == False:
        Chart.objects.create(product=data, name=data.title, price=data.price, update=data.update)


post_save.connect(product_post_save, sender=Product)


# ====================================================================================================

class Slider(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField(default=None)
    body = models.TextField()
    image = models.ImageField(upload_to='slider')
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title