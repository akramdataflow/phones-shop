from django.shortcuts import render


def about_page(request):
    return render(request, 'about.html')

def contact_page(request):
    return render(request, 'contact.html')