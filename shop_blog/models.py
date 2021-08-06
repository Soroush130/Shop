from django.db import models
from django import forms
from shop_account.models import UserAccount
from shop_product.models import Product


# Create your models here.


class Blog(models.Model):
    author = models.ForeignKey(UserAccount, on_delete=models.CASCADE, default=None)
    title = models.CharField(max_length=255)
    text = models.TextField()
    image = models.ImageField(upload_to='blog')
    create_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_first_half_text(self):
        return self.text[0:500]

    def get_second_half_text(self):
        return self.text[501:1000]


class RateBlog(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'blog : {self.blog.title} , rate : {self.rate}'


class RateBlogForm(forms.ModelForm):
    class Meta:
        model = RateBlog
        fields = ['rate']


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="blog_comment" ,default=None)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="user_comment")
    comment = models.TextField()
    create_on = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='reply_comment')
    is_reply = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
