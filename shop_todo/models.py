from django.db import models
from shop_account.models import UserAccount
from django import forms


# Create your models here.


class ToDo(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    text = models.CharField(max_length=1000)
    time = models.TimeField()
    date = models.DateField()
    active = models.BooleanField(default=True)


class ToDoForm(forms.Form):
    text = forms.CharField(max_length=1000)
    time = forms.TimeField(widget=forms.TimeInput())
    date = forms.DateField(widget=forms.DateInput())
