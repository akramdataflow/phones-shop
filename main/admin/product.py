from django.contrib import admin

from main.models import Product, ProductVariant, ProductImage


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ('image', 'order')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline, ProductImageInline]
    list_display = ('name', 'category', 'price', 'has_size', 'has_color')
    list_filter = ('category', 'price', 'has_size', 'has_color')
    search_fields = ('name', 'category__title', 'description',  'price')
    ordering = ('category', 'name')
