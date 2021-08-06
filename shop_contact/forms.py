from django import forms

from shop_contact.models import ContactUs


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['subject', 'message']
