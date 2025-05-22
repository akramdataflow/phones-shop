from main.models import Review
from django.contrib import admin

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'body')
    list_filter = ('rating',)
    search_fields = ('user__email', 'product__name')
