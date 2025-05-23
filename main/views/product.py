from django.shortcuts import render, get_object_or_404

from main.models import Product


def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'product.html', context)

def product_details(request, slug):
    product = get_object_or_404(
        Product.objects.select_related(
            'category', 'brand'
        ).prefetch_related(
            'productvariant_set', 'productimage_set',
        ),
        slug=slug
    )
    context = {
        'product': product,
        'images': product.productimage_set.all(),  # type: ignore
    }
    return render(request, 'product_details.html', context)
