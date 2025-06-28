from django.contrib import admin

from core.models import Color


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'hex_value')
    search_fields = ('name', 'number', 'hex_value')
