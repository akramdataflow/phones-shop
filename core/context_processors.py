from core.models import Brand, Category

# We have removed @lru_cache to ensure this function runs on every request.

def site_common(request):
    """
    Provides common context data to all templates,
    including 5 random brands for the footer.
    """
    
    # THE FIX IS HERE:
    # 1. order_by('?') sorts the brands randomly.
    # 2. [:5] selects the first 5 brands from the random list.
    random_brands = Brand.objects.order_by('?')[:5]
    
    # The categories can remain as they were, ordered by name.
    top_categories = Category.objects.all().order_by('name')

    return {
        'top_brands': random_brands,
        'top_categories': top_categories,
    }