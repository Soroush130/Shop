from django.db import models


# Create your models here.
from shop_account.models import UserAccount


class ContactUs(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, default=None)
    subject = models.CharField(max_length=250)
    message = models.TextField()
    create_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    phone = models.IntegerField()
    fax = models.IntegerField()
    address = models.CharField(max_length=500)
    email = models.EmailField()
    about_us = models.TextField()
    image = models.ImageField(upload_to='aboutus', null=True, blank=True)

    def get_first_half_text(self):
        return self.about_us[0:250]

    def get_second_half_text(self):
        return self.about_us[251:500]


