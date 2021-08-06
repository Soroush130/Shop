from django.contrib import admin

# Register your models here.
from shop_account.models import UserAccount, Profile

admin.site.register(UserAccount)
admin.site.register(Profile)
