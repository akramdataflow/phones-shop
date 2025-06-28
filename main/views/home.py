from django.shortcuts import render

from main.models import Product

def home(request):
    products = Product.objects.filter(is_featured=True)
    context = {
        'featured_products': products,
    }
    return render(request, 'home.html', context)
