from django.contrib import admin

from main.models import Product, ProductVariant


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductVariantInline]
    list_display = ('name', 'category', 'price', 'has_size', 'has_color')
    list_filter = ('category', 'price', 'has_size', 'has_color')
    search_fields = ('name', 'category__title', 'description',  'price')
    ordering = ('category', 'name')
