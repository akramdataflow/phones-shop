import uuid

from django.db import models
from django.conf import settings

from autoslug import AutoSlugField


def file_upload(instance, filename):
    file_name, extension = filename.split('.')
    return f"profile/{uuid.uuid4().hex}_{file_name}.{extension}"


class Profile(models.Model):
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    email = models.EmailField(max_length=254)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to=file_upload, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True)
    """
    Billing Information fields
    """
    IDENTIFICATION_TYPE_CHOICES = (
        ('00', 'Passport'),
        ('01', 'National ID'),
        ('02', 'Driving License'),
        ('03', 'Government Issued'),
        ('04', 'Other'),
    )
    CITIES = (
        ('BAGHDAD', 'Baghdad'),
        ('BASE', 'Base'),
        ('DHI', 'Dhi'),
        ('ERBIL', 'Erbil'),
        ('HALABJA', 'Halabja'),
        ('KARBI', 'Karbi'),
        ('KURD', 'Kurd'),
        ('MAYADAN', 'Mayadan'),
        ('MAYMARA', 'Maymara'),
        ('NINAWA', 'Ninawa'),
        ('SALAHALDIN', 'Salahaldin'),
        ('SULLA', 'Sulla'),
        ('WASIT', 'Wasit'),
    )
    account_id = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=20, choices=CITIES, null=True, blank=True)
    province_code = models.CharField(max_length=10, null=True, blank=True)
    postal_code = models.CharField(max_length=8, null=True, blank=True)
    country_code = models.CharField(max_length=2, default='IQ')
    birth_date = models.DateField(null=True, blank=True)
    identification_type = models.CharField(max_length=2, choices=IDENTIFICATION_TYPE_CHOICES, default='04')
    identification_number = models.CharField(max_length=12,  null=True, blank=True)
    identification_country_code = models.CharField(max_length=2,  default='IQ')
    identification_expiration_date = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=2, default='IQ')
    country_of_birth = models.CharField(max_length=2, default='IQ')

    def __str__(self):
        return self.name
    
    def masked_email(self):
        return f"{self.email[:2]}...{self.email[-2:]}"
    
    def masked_phone_number(self):
        return f"{self.phone_number[:2]}...{self.phone_number[-2:]}"
    
    def validate_billing_information(self) -> bool:
        return all([
            self.name,
            self.phone_number,
            self.email,
            # self.account_id,
            # self.account_number,
            self.address,
            self.city,
            self.province_code,
            self.postal_code,
            self.country_code,
            self.birth_date,
            # self.identification_type,
            # self.identification_number,
            # self.identification_country_code,
            # self.identification_expiration_date,
            self.nationality,
            self.country_of_birth,
        ])