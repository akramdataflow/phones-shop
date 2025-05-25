from core.models import Brand, Category

from functools import lru_cache

@lru_cache
def site_common(request):
    return {
        'top_brands': Brand.objects.all().order_by('name'),
        'top_categories': Category.objects.all().order_by('name'),
    }