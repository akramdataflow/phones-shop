from django.contrib import admin
from ..models import Brand

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Brands with multilingual support.
    """
    # Fields to display in the list view
    list_display = ('id', 'name', 'name_ar', 'slug')
    
    # Fields that can be edited directly from the list view
    list_editable = ('name', 'name_ar')
    
    # Fields to search by
    search_fields = ('name', 'name_ar')
    
    # Automatically generate the slug from the primary name field
    prepopulated_fields = {'slug': ('name',)}