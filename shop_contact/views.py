from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
from shop_contact.forms import ContactForm
from shop_contact.models import ContactUs, AboutUs


def contact_page(request):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            ContactUs.objects.create(user_id=request.user.id, subject=data['subject'], message=data['message'])
            return redirect(url)
        else:
            return HttpResponse('فرم را با دقت پر کنید')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'contact/contact-us.html', context)


def about_page(request):
    about_us = AboutUs.objects.filter().first()
    return render(request, 'about-us/about.html', {'about_us': about_us})
