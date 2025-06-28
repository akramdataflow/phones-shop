from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from main.models import Product
from core.models import Brand, Category


def product_list(request):

    products = Product.objects.all().order_by('-id')
    brands = Brand.objects.filter(product__in=products.values_list('id')).distinct()
    categories = Category.objects.filter(product__in=products.values_list('id')).distinct()

    selected_brands = request.GET.getlist('brand')
    selected_categories = request.GET.getlist('category')

    if selected_brands:
        products = products.filter(brand__slug__in=selected_brands)
    if selected_categories:
        products = products.filter(category__slug__in=selected_categories)

    product_count = products.count()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'products': page_obj,
        'selected_brands': selected_brands,
        'selected_categories': selected_categories,
        'brands': brands,
        'categories': categories,
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

