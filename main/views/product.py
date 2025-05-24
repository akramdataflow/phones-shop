from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from main.models import Product


def product_list(request):
    products = Product.objects.all().order_by('-id')
    product_count = products.count()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'products': page_obj,
        'product_count': product_count,
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

