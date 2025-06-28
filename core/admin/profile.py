from django.contrib import admin
from core.models.profile import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'name', 'email', 'phone_number', 'city', 'country_code',
        'birth_date', 'nationality', 'country_of_birth'
    ]
    search_fields = ['name', 'email', 'phone_number', 'account_id', 'account_number']
    list_filter = ['city', 'country_code', 'nationality', 'country_of_birth']
    readonly_fields = ['slug']
