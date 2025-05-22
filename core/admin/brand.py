from core.models import Brand
from django.contrib import admin


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug',)
    list_editable = ('name',)