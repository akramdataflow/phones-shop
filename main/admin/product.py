from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from ..models import Product, ProductVariant, ProductImage

#------------------------------------------------
# 1. Inline for Product Variants (Colors & Sizes)
#------------------------------------------------
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    fields = ('color', 'size', 'quantity', 'price')
    extra = 1
    verbose_name = _("Stock and Variant")
    verbose_name_plural = _("Stock and Variants (Colors, Sizes)")

#------------------------------------------------
# 2. Inline for Product Images
#------------------------------------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'order')
    verbose_name = _("Product Image")
    verbose_name_plural = _("Product Images")

#------------------------------------------------
# 3. The Main Admin Configuration for Products
#------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Final and simplified admin interface for the Product model.
    """
    
    # --- List View Configuration ---
    list_display = ('name', 'name_ar', 'brand', 'category', 'price', 'is_featured')
    list_filter = ('is_featured', 'brand', 'category')
    search_fields = ('name', 'name_ar', 'brand__name')
    ordering = ('-id',)

    # --- Form View Configuration ---
    # ==============================================================
    # THE FINAL FIX: 'slug' has been COMPLETELY REMOVED from fieldsets.
    # It will be generated automatically in the background upon saving.
    # ==============================================================
    fieldsets = (
        (_("English Content"), {
            'fields': ('name', 'description')
        }),
        (_("Arabic Content"), {
            'fields': ('name_ar', 'description_ar'),
            'classes': ('collapse',),
        }),
        (_("Core Details"), {
            'fields': ('price', 'currency', 'brand', 'category', 'image')
        }),
        (_("Settings & Options"), {
            'fields': ('is_featured', 'label', 'has_color', 'has_size')
        }),
    )

    inlines = [ProductVariantInline, ProductImageInline]
    
    # NOTE: prepopulated_fields and readonly_fields have been removed
    # to eliminate all possible conflicts. The AutoSlugField will handle
    # the slug generation automatically when you save the product.