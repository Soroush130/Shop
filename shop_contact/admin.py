from django.contrib import admin

# Register your models here.
from shop_contact.models import ContactUs, AboutUs


class ContactAdmin(admin.ModelAdmin):
    list_filter = ['subject']
    list_display = ['user', 'subject']


admin.site.register(ContactUs, ContactAdmin)
admin.site.register(AboutUs)
