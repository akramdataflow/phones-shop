from django.contrib import admin

from core.models import Size


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('size', 'unit')
    list_filter = ('unit',)
    ordering = ('unit',)
